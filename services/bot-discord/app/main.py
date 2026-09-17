#!/usr/bin/python3
import os
import sys
import logging
import discord
from discord.ext import commands
from discord import app_commands
from typing import Literal, Optional
from modules import *
from modules.orchestrator import *
from modules.administrator import *
from modules.user import *
from modules.shared import *

print("\n------------------------------\nStarting Discord Bot...\n------------------------------\n")
configure_logging()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

class PeonBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=settings.get('command_prefix', '!'),
            intents=intents,
            help_command=None
        )
        self._startup_tasks_done = False
    
    async def setup_hook(self):
        """Called when the bot is starting up"""
        # The per-server control panel's buttons encode gameuid/servername/action in their
        # custom_id, so this registers the *class* once (not a per-server instance) and
        # discord.py reconstructs+dispatches the right button via PersistentServerButton
        # .from_custom_id whenever an interaction arrives with no live view in memory
        # (e.g. after this exact restart). See modules/user.py for the implementation.
        self.add_dynamic_items(PersistentServerButton)
        logging.info("Registered persistent server-panel buttons")
    
    async def on_ready(self):
        if self._startup_tasks_done:
            logging.info(f"Connected as @{self.user.name}. Startup tasks already completed.")
            return

        logging.info(f'Connected as bot named @{self.user.name}. Running PEON init tasks...')
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logging.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            logging.error(f"Failed to sync commands: {e}")
        
        # Clean channels
        for guild in self.guilds:
            for channel in guild.text_channels:
                try:
                    permissions = channel.permissions_for(guild.me)
                    if permissions.send_messages and permissions.read_message_history and permissions.manage_messages:
                        await clean_channel(channel, self.user, limit=100)
                except Exception as exc:
                    logging.warning(f"Skipping clean in #{channel.name}: {exc}")
        
        # Notify admin channel
        for guild in self.guilds:
            admin_channel = discord.utils.get(guild.text_channels, name=settings['control_channel'])
            if admin_channel:
                embed = discord.Embed(
                    title="🤖 PEON Bot Ready",
                    description="Bot has connected and is ready for commands!",
                    color=discord.Color.green()
                )
                try:
                    await admin_channel.send(embed=embed)
                except Exception as exc:
                    logging.warning(f"Failed to notify admin channel in {guild.name}: {exc}")
                break

        self._startup_tasks_done = True

bot = PeonBot()

async def clean_channel(channel, bot_user, limit=10):
    try:
        async for message in channel.history(limit=limit):
            if (message.author == bot_user and message.embeds):
                first_embed = message.embeds[0]
                if first_embed.image and first_embed.image.url == bot_image:
                    await message.delete()
            elif (message.content.startswith(settings.get('command_prefix', '!')) and message.author != bot_user): 
                await message.delete()
        return True
    except Exception as e:
        logging.error(f"Error cleaning channel {channel.name}: {e}")
        return False

# Autocomplete functions
async def server_autocomplete(interaction: discord.Interaction, current: str):
    """Autocomplete for server names"""
    try:
        if 'error' in (result := get_peon_orcs())['status']:
            return []
        
        all_servers = []
        for orchestrator in result['data']:
            try:
                servers = get_servers(orchestrator['url'], orchestrator['key'])
                for server in servers:
                    server_name = f"{server.get('game_uid', '')}.{server.get('servername', '')}"
                    all_servers.append(app_commands.Choice(name=server_name, value=server_name))
            except:
                continue
        
        # Filter based on current input
        filtered = [choice for choice in all_servers if current.lower() in choice.name.lower()][:25]
        return filtered
    except:
        return []

async def game_type_autocomplete(interaction: discord.Interaction, current: str):
    """Autocomplete for game types"""
    try:
        if 'error' in (result := get_peon_orcs())['status']:
            return []
        
        if not result['data']:
            return []

        orchestrator = result['data'][0]
        plans_result = get_all_plans(orchestrator['url'], orchestrator['key'])
        
        if plans_result['status'] != 'success':
            return []
        
        game_types = []
        for plan in plans_result['data']:
            game_uid = plan.get('game_uid', '')
            title = plan.get('title', game_uid)
            if game_uid:
                game_types.append(app_commands.Choice(name=f"{title} ({game_uid})", value=game_uid))
        
        # Filter based on current input
        filtered = [choice for choice in game_types if current.lower() in choice.name.lower()][:25]
        return filtered
    except:
        return []

# Slash Commands
@bot.tree.command(name="peon", description="🤖 Summon a peon for server management")
@app_commands.describe(
    channel_type="Specify channel type (admin/server) or let bot auto-detect"
)
async def peon_slash(
    interaction: discord.Interaction, 
    channel_type: Optional[Literal["admin", "server"]] = None
):
    await interaction.response.defer()
    
    # Auto-detect channel type if not specified
    if not channel_type:
        if str(interaction.channel.name) == settings['control_channel']:
            channel_type = "admin"
        else:
            try:
                if parse_server_channel_name(str(interaction.channel.name)):
                    channel_type = "server"
                else:
                    channel_type = "admin"
            except:
                channel_type = "admin"
    
    embed = discord.Embed(
        title="🛡️ PEON Reporting for Duty",
        description=f"*{get_quote()}*",
        color=discord.Color.green()
    )
    embed.set_image(url=bot_image)

    if channel_type == "admin":
        # NOTE: there is no dedicated admin button panel (yet) -- the administrative
        # actions available today are the /server, /create, /list, and /debug slash
        # commands. This branch used to reference an EnhancedAdministratorView class
        # that was never defined anywhere in the codebase, which raised a NameError
        # on every use; send the informational embed without a view instead of
        # inventing button actions nobody has specified.
        embed.add_field(
            name="🔧 Admin Mode",
            value="Use `/server`, `/create`, `/list`, or `/debug` for administrative actions.",
            inline=False,
        )
        embed.set_footer(text="Try /help for the full command list")
        await interaction.followup.send(embed=embed)
    else:
        try:
            channel_name = str(interaction.channel.name)
            parsed = parse_server_channel_name(channel_name)
            if not parsed:
                raise ValueError(f"Invalid channel name: {channel_name}")
            gameuid, servername = parsed
            view = build_persistent_user_panel(gameuid, servername)
            embed.add_field(name="🎮 Server Mode", value=f"Managing **{gameuid}.{servername}**", inline=False)
            embed.set_footer(text="Use the buttons below or try /help for more commands")
            await interaction.followup.send(embed=embed, view=view)
        except:
            embed = build_card(status='nok', message="❌ This doesn't look like a warcamp channel!\n\nChannels should be named: `game-servername`")
            await interaction.followup.send(embed=embed)

@bot.tree.command(name="server", description="🎮 Quick server management commands")
@app_commands.describe(
    action="What action to perform on the server",
    server="Server to target (auto-complete available)",
    timer="For stop: time/duration (e.g., 15m, 2h, 22:00)",
    mode="For update: update mode (server/image/full/reinit)"
)
@app_commands.autocomplete(server=server_autocomplete)
async def server_command(
    interaction: discord.Interaction,
    action: Literal["start", "stop", "restart", "info", "update", "backup"],
    server: str = None,
    timer: Optional[str] = None,
    mode: Optional[Literal["server", "image", "full", "reinit"]] = None
):
    await interaction.response.defer()
    
    # Auto-detect server from channel if not provided
    if not server:
        try:
            channel_name = str(interaction.channel.name)
            parsed = parse_server_channel_name(channel_name)
            if not parsed:
                raise ValueError(f"Invalid channel name: {channel_name}")
            gameuid, servername = parsed
            server = f"{gameuid}.{servername}"
        except:
            embed = build_card(status='nok', message="❌ Could not auto-detect server from channel name.\nPlease specify server parameter.")
            await interaction.followup.send(embed=embed)
            return
    
    # Build args for server_actions function
    server_parts = server.split('.')
    if len(server_parts) != 2:
        embed = build_card(status='nok', message="❌ Server format should be: `game.servername`")
        await interaction.followup.send(embed=embed)
        return
    
    args = [server_parts[0], server_parts[1]]  # gameuid, servername
    
    if timer and action == "stop":
        args.append(timer)
    elif mode and action == "update":
        args.append(mode)
    
    # Handle special cases
    if action == "backup":
        if 'error' in (result := get_peon_orcs())['status']:
            embed = build_card(status='nok', message="No orchestrators registered")
            await interaction.followup.send(embed=embed)
            return
        
        orchestrator = result['data'][0]
        backup_result = server_get_save_download(orchestrator['url'], orchestrator['key'], server)
        
        if backup_result['status'] == 'success':
            embed = build_card(
                status='ok',
                title="📦 Server Backup Ready",
                message=f"Backup for **{server}** is ready!\n\n🔗 [Download Here]({backup_result['download_url']})"
            )
        else:
            embed = build_card(status='nok', message=f"Backup failed: {backup_result.get('message', 'Unknown error')}")
        
        await interaction.followup.send(embed=embed)
        return
    
    # Execute server action
    response = server_actions(action=action, args=args)
    username = interaction.user.display_name
    
    if response['status'] == 'success':
        if action == 'info':
            embed = build_card(status='ok', title=f"📊 {server} Status", message=response['data'])
        else:
            embed = build_card(
                status='ok',
                title=f"✅ Server {action.title()} Complete",
                message=f"**{action.upper()}** action completed for **{server}** by *@{username}*"
            )
    else:
        embed = build_card(
            status='nok',
            title=f"❌ Server {action.title()} Failed",
            message=f"Error: {response.get('err_code', 'Unknown error')}"
        )
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="create", description="🏗️ Create a new game server")
@app_commands.describe(
    game_type="Type of game server to create",
    server_name="Name for the new server",
    description="Optional description for the server"
)
@app_commands.autocomplete(game_type=game_type_autocomplete)
async def create_server(
    interaction: discord.Interaction,
    game_type: str,
    server_name: str,
    description: Optional[str] = None
):
    await interaction.response.defer()
    
    if 'error' in (result := get_peon_orcs())['status']:
        embed = build_card(status='nok', message="No orchestrators registered")
        await interaction.followup.send(embed=embed)
        return
    
    orchestrator = result['data'][0]
    user_settings = {}
    if description:
        user_settings['description'] = description
    
    create_result = server_create(
        orchestrator['url'],
        orchestrator['key'],
        game_type,
        server_name,
        user_settings
    )
    
    if create_result['status'] == 'success':
        embed = build_card(
            status='ok',
            title="🎉 Server Created Successfully!",
            message=f"**{game_type}.{server_name}** has been created!\n\n🎮 Game: {game_type}\n📝 Name: {server_name}"
        )
        if description:
            embed.add_field(name="📄 Description", value=description, inline=False)
    else:
        # Check if it's a plan availability issue
        error_message = create_result.get('message', 'Unknown error')
        
        # Add additional debugging for 404 errors
        if '404' in error_message or 'NOT FOUND' in error_message:
            # Check available plans
            plans_result = get_all_plans(orchestrator['url'], orchestrator['key'])
            if plans_result['status'] == 'success':
                available_games = [p.get('game_uid', '') for p in plans_result.get('data', []) if isinstance(p, dict)]
                if game_type not in available_games and available_games:
                    error_message += f"\n\n**Available games:** {', '.join(available_games)}"
            else:
                error_message += f"\n\n**Connectivity issue detected.** Use `/debug test_connectivity` to diagnose."
        
        embed = build_card(
            status='nok',
            title="❌ Server Creation Failed",
            message=f"There was an issue creating your server.\n\n**Error Details**\n{error_message}"
        )
    
    # Replace the deferred interaction with the result
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="list", description="📋 List servers and orchestrators")
@app_commands.describe(
    list_type="What to list"
)
async def list_command(
    interaction: discord.Interaction,
    list_type: Literal["servers", "orchestrators", "plans"]
):
    await interaction.response.defer()
    
    if list_type == "orchestrators":
        if 'error' in (result := get_peon_orcs())['status']:
            embed = build_card(status='nok', message="No orchestrators registered")
        else:
            orcs_text = "**Registered Orchestrators:**\n"
            for orc in result['data']:
                # Test connection
                orc_details = await get_orchestrator_details_async(orc['url'], orc['key'])
                status = "🟢 Online" if orc_details['status'] == 'success' else "🔴 Offline"
                orcs_text += f"• **{orc['name']}** - {status}\n  📡 {orc['url']}\n"
            embed = build_card(status='ok', title="🏢 Orchestrators", message=orcs_text)
    
    elif list_type == "plans":
        if 'error' in (result := get_peon_orcs())['status']:
            embed = build_card(status='nok', message="No orchestrators registered")
            await interaction.followup.send(embed=embed)
            return
        
        orchestrator = result['data'][0]
        plans_result = get_all_plans(orchestrator['url'], orchestrator['key'])
        
        if plans_result['status'] == 'success':
            plans_text = "**Available Game Plans:**\n"
            for plan in plans_result['data'][:15]:  # Limit for embed
                title = plan.get('title', 'Unknown')
                game_uid = plan.get('game_uid', 'unknown')
                plans_text += f"🎮 **{title}** (`{game_uid}`)\n"
            
            if len(plans_result['data']) > 15:
                plans_text += f"\n... and {len(plans_result['data']) - 15} more plans"
            
            embed = build_card(status='ok', title="📚 Game Plans", message=plans_text)
        else:
            embed = build_card(status='nok', message="Failed to get plans list")
    
    else:  # servers
        if 'error' in (result := get_peon_orcs())['status']:
            embed = build_card(status='nok', message="No orchestrators registered")
        else:
            servers_text = "**All Servers:**\n"
            for orchestrator in result['data']:
                try:
                    servers = get_servers(orchestrator['url'], orchestrator['key'])
                    servers_text += f"\n**🏢 {orchestrator['name']}:**\n"
                    for server in servers:
                        status_emoji = "🟢" if server.get('server_state', '').lower() == 'running' else "🔴"
                        game_type = server.get('game_uid', 'unknown')
                        name = server.get('servername', 'unknown')
                        servers_text += f"  {status_emoji} **{game_type}.{name}** [{server.get('server_state', 'unknown')}]\n"
                except:
                    servers_text += f"\n**🏢 {orchestrator['name']}:** (unavailable)\n"
            
            embed = build_card(status='ok', title="🖥️ Server Status", message=servers_text)
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="about", description="ℹ️ Show information about PEON Bot")
async def about_command(interaction: discord.Interaction):
    await interaction.response.send_message(embed=await build_about_card())

@bot.tree.command(name="help", description="❓ Show help information")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 PEON Bot Help",
        description="Welcome to the PEON Project Discord Bot!",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🎮 Server Commands",
        value="• `/server` - Quick server actions\n• `/create` - Create new servers\n• `/list servers` - Show all servers",
        inline=False
    )
    
    embed.add_field(
        name="🏢 Management Commands",
        value="• `/peon` - Main interface\n• `/list orchestrators` - Show orchestrators\n• `/list plans` - Show game plans",
        inline=False
    )
    
    embed.add_field(
        name="💡 Tips",
        value="• Use `/peon` in admin channels for full controls\n• Use `/peon` in game channels for server controls\n• Most commands support auto-completion",
        inline=False
    )
    
    embed.set_footer(text="Use slash commands (/) for the best experience!")
    await interaction.response.send_message(embed=embed)

# Legacy support for existing prefix commands (optional)
@bot.command(name='peon')
async def legacy_peon(ctx):
    embed = discord.Embed(
        title="🔄 Command Updated!",
        description="This bot now uses **Slash Commands** for a better experience!\n\n✨ Try `/peon` instead of `!peon`",
        color=discord.Color.gold()
    )
    embed.add_field(name="🚀 New Features", value="• Auto-completion\n• Better help system\n• Cleaner interface", inline=False)
    await ctx.send(embed=embed, delete_after=10)

@bot.tree.command(name="debug", description="🔧 Debug orchestrator connectivity and plans")
@app_commands.describe(
    action="Debug action to perform"
)
@app_commands.choices(action=[
    app_commands.Choice(name="test_connectivity", value="test_connectivity"),
    app_commands.Choice(name="list_plans", value="list_plans")
])
async def debug_command(
    interaction: discord.Interaction,
    action: str
):
    await interaction.response.defer()
    
    if 'error' in (result := get_peon_orcs())['status']:
        embed = build_card(status='nok', message="No orchestrators registered")
        await interaction.followup.send(embed=embed)
        return
    
    orchestrator = result['data'][0]
    
    if action == "test_connectivity":
        from modules.orchestrator import test_orchestrator_connectivity
        test_result = test_orchestrator_connectivity(orchestrator['url'], orchestrator['key'])
        
        if test_result['status'] == 'success':
            available_plans = test_result.get('available_plans', [])
            if available_plans and isinstance(available_plans[0], dict):
                available_plan_text = ', '.join([p.get('game_uid', '?') for p in available_plans])
            else:
                available_plan_text = ', '.join([str(p) for p in available_plans])
            embed = build_card(
                status='ok',
                title="🔧 Orchestrator Connectivity Test",
                message=f"**Connection Status:** ✅ Connected\n**Available Plans:** {available_plan_text or 'None detected'}"
            )
        else:
            embed = build_card(
                status='nok',
                title="🔧 Orchestrator Connectivity Test",
                message=f"**Connection Failed:** {test_result.get('message', 'Unknown error')}"
            )
    
    elif action == "list_plans":
        plans_result = get_all_plans(orchestrator['url'], orchestrator['key'])
        
        if plans_result['status'] == 'success':
            plans_data = plans_result.get('data', [])
            if plans_data and isinstance(plans_data[0], dict):
                plan_text = ', '.join([p.get('game_uid', '?') for p in plans_data])
            else:
                plan_text = ', '.join([str(p) for p in plans_data])
            embed = build_card(
                status='ok',
                title="📋 Available Game Plans",
                message=f"**Available Games:** {plan_text or 'None detected'}"
            )
        else:
            embed = build_card(
                status='nok',
                title="📋 Available Game Plans",
                message=f"**Error:** {plans_result.get('message', 'Unknown error')}"
            )
    
    await interaction.followup.send(embed=embed)

# Error handling
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        embed = build_card(status='nok', message=f"⏰ Command on cooldown. Try again in {error.retry_after:.2f} seconds.")
    elif isinstance(error, app_commands.MissingPermissions):
        embed = build_card(status='nok', message="❌ You don't have permission to use this command.")
    else:
        embed = build_card(status='nok', message=f"❌ An error occurred: {str(error)}")
        logging.error(f"App command error: {error}")
    
    try:
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
    except:
        pass

# MAIN
if __name__ == "__main__":
    TOKEN = os.environ.get('DISCORD_TOKEN', None)
    if TOKEN:
        bot.run(TOKEN)
    else:
        logging.critical("Please create and configure a valid Discord token.")
        sys.exit(2)