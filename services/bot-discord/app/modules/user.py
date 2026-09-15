import logging
import discord
from typing import Optional
from . import *
from .shared import *
from .orchestrator import *

class PersistentUserView(discord.ui.View):
    """Persistent view that survives bot restarts"""
    def __init__(self):
        super().__init__(timeout=None)

class EnhancedUserView(discord.ui.View):
    """Enhanced user interface with better UX, dynamic buttons, and visual feedback"""
    def __init__(self, gameuid: str, servername: str):
        self.gameuid = gameuid
        self.servername = servername
        super().__init__(timeout=300)  # 5 minute timeout
        
        # Get current server status to set dynamic button states
        self._update_button_states()
        
    def _update_button_states(self):
        """Update button states based on current server status"""
        try:
            if 'error' in (result := get_peon_orcs())['status']:
                return
            
            # Get current server status
            args = [self.gameuid, self.servername]
            response = server_actions(action='get', args=args)
            
            if response['status'] == 'success':
                # This could be used to disable/enable buttons based on server state
                # For now, we'll keep all buttons enabled
                pass
        except:
            pass
    
    def _disable_all_buttons(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

    async def _handle_server_action(self, interaction: discord.Interaction, action: str, show_feedback: bool = True):
        """Enhanced server action handler with better feedback"""
        if show_feedback:
            self._disable_all_buttons()
            await interaction.response.edit_message(view=self)
        
        username = str(interaction.user.display_name)
        server_name = f"{self.gameuid}.{self.servername}"
        
        logging.info(f"Server {action.upper()} triggered by <@{interaction.user}> for {server_name}")
        
        response = server_actions(action=action, args=[self.gameuid, self.servername])
        
        if response['status'] == 'success':
            if action == 'get':
                embed = discord.Embed(
                    title=f"📊 {server_name} Status",
                    description=response['data'],
                    color=discord.Color.blue()
                )
                # Add server status emoji to title based on content
                if "running" in response['data'].lower():
                    embed.title = f"🟢 {server_name} Status"
                elif "exited" in response['data'].lower() or "stopped" in response['data'].lower():
                    embed.title = f"🔴 {server_name} Status"
                else:
                    embed.title = f"🟡 {server_name} Status"
            else:
                # Action-specific emojis and messages
                action_info = {
                    'start': {'emoji': '🚀', 'desc': 'Server is starting up!'},
                    'stop': {'emoji': '🛑', 'desc': 'Server is shutting down!'},
                    'restart': {'emoji': '🔄', 'desc': 'Server is restarting!'},
                    'update': {'emoji': '⬆️', 'desc': 'Server is updating!'}
                }
                
                info = action_info.get(action, {'emoji': '✅', 'desc': f'{action.title()} completed!'})
                
                embed = discord.Embed(
                    title=f"{info['emoji']} {action.title()} Initiated",
                    description=f"**{server_name}** - {info['desc']}\n\n*Requested by @{username}*",
                    color=discord.Color.green()
                )
        else:
            error_messages = {
                'srv.param': 'Invalid server parameters provided',
                'orc.none': 'No orchestrators are registered',
                'srv.dne': 'Server not found',
                'srv.notexplicit': 'Multiple servers found - be more specific',
                'orc.notavailable': 'Orchestrator is not available'
            }
            
            error_msg = error_messages.get(
                response.get('err_code'), 
                response.get('err_code', 'Unknown error occurred')
            )
            
            embed = discord.Embed(
                title=f"❌ {action.title()} Failed",
                description=f"**{server_name}**\n\n{error_msg}",
                color=discord.Color.red()
            )
            embed.add_field(
                name="💡 Troubleshooting",
                value="• Check server name spelling\n• Verify orchestrator is online\n• Try `/list servers` to see available servers",
                inline=False
            )
        
        if show_feedback:
            await replace_interaction_with_result(interaction, embed)
        else:
            return embed

    @discord.ui.button(label="🚀 Start", style=discord.ButtonStyle.success, row=0)
    async def server_start(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._handle_server_action(interaction, 'start')
        
    @discord.ui.button(label="🔄 Restart", style=discord.ButtonStyle.secondary, row=0)
    async def server_restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._handle_server_action(interaction, 'restart')

    @discord.ui.button(label="🛑 Stop", style=discord.ButtonStyle.danger, row=0)
    async def server_stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EnhancedStopTimerModal(self.gameuid, self.servername))
        await remove_interactions(interaction)
    
    @discord.ui.button(label="📊 Info", style=discord.ButtonStyle.secondary, row=1)
    async def server_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._handle_server_action(interaction, 'get')
    
    @discord.ui.button(label="⬆️ Update", style=discord.ButtonStyle.secondary, row=1)
    async def server_update(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._disable_all_buttons()
        await interaction.response.edit_message(view=self)
        
        view = discord.ui.View(timeout=60)
        view.add_item(EnhancedUpdateModeSelect(self.gameuid, self.servername))
        
        embed = discord.Embed(
            title="⬆️ Server Update Options",
            description=f"Select update type for **{self.gameuid}.{self.servername}**:",
            color=discord.Color.orange()
        )
        embed.add_field(
            name="⚠️ Important",
            value="Updates may require the server to be stopped. Choose the appropriate update type:",
            inline=False
        )
        
        await interaction.followup.send(embed=embed, view=view)

    @discord.ui.button(label="📦 Backup", style=discord.ButtonStyle.primary, row=1)
    async def server_backup(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._disable_all_buttons()
        await interaction.response.edit_message(view=self)
        
        # Get orchestrator info
        if 'error' in (result := get_peon_orcs())['status']:
            embed = build_card(status='nok', message="No orchestrators registered")
            await interaction.channel.send(embed=embed)
            await remove_interactions(interaction)
            return
        
        server_uid = f"{self.gameuid}.{self.servername}"
        orchestrator = result['data'][0]  # Use first orchestrator for now
        
        backup_result = server_get_save_download(
            orchestrator['url'],
            orchestrator['key'],
            server_uid
        )
        
        if backup_result['status'] == 'success':
            embed = discord.Embed(
                title="📦 Server Backup Ready",
                description=f"Backup for **{server_uid}** has been prepared!",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="📥 Download",
                value=f"[Click here to download backup]({backup_result['download_url']})",
                inline=False
            )
            embed.add_field(
                name="📋 Contents",
                value="• Server configuration files\n• Player data and progress\n• World/map files",
                inline=False
            )
            embed.set_footer(text="Backup files are compressed and ready for download")
        else:
            embed = discord.Embed(
                title="❌ Backup Failed",
                description=f"Could not create backup for **{server_uid}**",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Error Details",
                value=backup_result.get('message', 'Unknown error occurred'),
                inline=False
            )
        
        await replace_interaction_with_result(interaction, embed)
        
    @discord.ui.button(label="📝 Edit Description", style=discord.ButtonStyle.secondary, row=2)
    async def edit_description(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = EnhancedEditDescriptionModal(self.gameuid, self.servername)
        await interaction.response.send_modal(modal)
        await remove_interactions(interaction)
        
    @discord.ui.button(label="🗑️ Delete Server", style=discord.ButtonStyle.danger, row=2)
    async def delete_server(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._disable_all_buttons()
        await interaction.response.edit_message(view=self)
        
        view = EnhancedDeleteConfirmView(self.gameuid, self.servername)
        embed = discord.Embed(
            title="⚠️ DANGER ZONE ⚠️",
            description=f"You are about to **DELETE** server:\n\n🎮 **{self.gameuid}.{self.servername}**",
            color=discord.Color.red()
        )
        embed.add_field(
            name="🚨 Warning",
            value="This action cannot be undone! Choose your deletion type carefully:",
            inline=False
        )
        embed.add_field(
            name="🗃️ Container Only",
            value="Removes only the server container. Player data and configs are preserved.",
            inline=True
        )
        embed.add_field(
            name="💥 Complete Deletion",
            value="Removes EVERYTHING including all player data, saves, and configurations.",
            inline=True
        )
        
        await interaction.followup.send(embed=embed, view=view)

    @discord.ui.button(label="ℹ️ About", style=discord.ButtonStyle.secondary, row=2)
    async def server_about(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._disable_all_buttons()
        await interaction.response.edit_message(content="*Getting system information...*", view=self)
        message = await interaction.channel.send(embed=await build_about_card())
        await remove_interactions(interaction, keep=message.id)

# Enhanced Modal Classes

class EnhancedStopTimerModal(discord.ui.Modal, title='🛑 Schedule Server Stop'):
    def __init__(self, gameuid: str, servername: str):
        super().__init__(title='🛑 Schedule Server Stop')
        self.gameuid = gameuid
        self.servername = servername
        
        self.stop_timer = discord.ui.TextInput(
            label='Stop Time/Duration (Optional)',
            style=discord.TextStyle.short,
            placeholder='Examples: 15m, 2h, 22:00, 2025/01/16.21h30 or leave empty for immediate stop',
            required=False,
            min_length=0,
            max_length=20
        )
        self.add_item(self.stop_timer)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        username = str(interaction.user.display_name)
        server_name = f"{self.gameuid}.{self.servername}"
        
        logging.info(f"Server STOP triggered by <@{interaction.user}> for {server_name}")
        
        args = [self.gameuid, self.servername]
        if self.stop_timer.value and self.stop_timer.value.strip():
            args.append(self.stop_timer.value.strip())
        
        response = server_actions(action='stop', args=args)
        
        if response['status'] == 'success':
            if self.stop_timer.value and self.stop_timer.value.strip():
                embed = discord.Embed(
                    title="⏰ Server Stop Scheduled",
                    description=f"**{server_name}** will stop in **{self.stop_timer.value.strip()}**",
                    color=discord.Color.orange()
                )
                embed.add_field(
                    name="📅 Scheduled By",
                    value=f"@{username}",
                    inline=True
                )
                embed.add_field(
                    name="⏲️ When",
                    value=self.stop_timer.value.strip(),
                    inline=True
                )
            else:
                embed = discord.Embed(
                    title="🛑 Server Stopping",
                    description=f"**{server_name}** is shutting down immediately",
                    color=discord.Color.red()
                )
                embed.add_field(
                    name="👤 Initiated By",
                    value=f"@{username}",
                    inline=True
                )
        else:
            embed = discord.Embed(
                title="❌ Stop Command Failed",
                description=f"Could not stop **{server_name}**",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Error",
                value=response.get('err_code', 'Unknown error'),
                inline=False
            )
        
        # Try to replace the original modal message with the result
        try:
            await interaction.edit_original_response(embed=embed, view=None)
        except:
            await interaction.followup.send(embed=embed)

class EnhancedUpdateModeSelect(discord.ui.Select):
    def __init__(self, gameuid: str, servername: str):
        self.gameuid = gameuid
        self.servername = servername
        
        options = [
            discord.SelectOption(
                label="🎮 Game Server Files",
                value="server",
                description="Update only the game server files (default & safest)",
                emoji="🎮"
            ),
            discord.SelectOption(
                label="📦 Container Image", 
                value="image",
                description="Update the PEON container that runs the game server",
                emoji="📦"
            ),
            discord.SelectOption(
                label="🔄 Complete Update",
                value="full", 
                description="Update both game server files AND container image",
                emoji="🔄"
            ),
            discord.SelectOption(
                label="🔥 Reinstall Server",
                value="reinit",
                description="Remove server files (keep saves) and reinstall completely",
                emoji="🔥"
            )
        ]
        
        super().__init__(
            placeholder='Select update type...',
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected_option = next(opt for opt in self.options if opt.value == self.values[0])
        
        view = EnhancedUpdateConfirmView(selected_option.value, self.gameuid, self.servername, selected_option.label)
        
        risk_levels = {
            'server': ('🟢', 'Low Risk', 'Safest option - only updates game files'),
            'image': ('🟡', 'Medium Risk', 'May require server restart'),
            'full': ('🟠', 'High Risk', 'Updates everything - server will restart'),
            'reinit': ('🔴', 'Very High Risk', 'Completely reinstalls server files')
        }
        
        risk_emoji, risk_level, risk_desc = risk_levels.get(selected_option.value, ('🟡', 'Unknown', ''))
        
        embed = discord.Embed(
            title=f"⚠️ Confirm {selected_option.label}",
            description=f"Are you sure you want to perform this update on **{self.gameuid}.{self.servername}**?",
            color=discord.Color.orange()
        )
        embed.add_field(
            name=f"{risk_emoji} Risk Level",
            value=f"**{risk_level}**\n{risk_desc}",
            inline=False
        )
        
        if selected_option.value == 'reinit':
            embed.add_field(
                name="🚨 IMPORTANT",
                value="This will DELETE all server files except player saves!",
                inline=False
            )
        
        await interaction.response.edit_message(embed=embed, view=view)

class EnhancedUpdateConfirmView(discord.ui.View):
    def __init__(self, mode: str, gameuid: str, servername: str, mode_label: str):
        super().__init__(timeout=30)
        self.mode = mode
        self.gameuid = gameuid
        self.servername = servername
        self.mode_label = mode_label
        
    def _disable_all_buttons(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

    @discord.ui.button(label="✅ Confirm Update", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._disable_all_buttons()
        await interaction.response.edit_message(view=self)
        
        username = str(interaction.user.display_name)
        server_name = f"{self.gameuid}.{self.servername}"
        
        logging.info(f"Server UPDATE ({self.mode.upper()}) triggered by <@{interaction.user}> for {server_name}")
        
        response = server_actions(action='update', args=[self.gameuid, self.servername, self.mode])
        
        if response['status'] == 'success':
            embed = discord.Embed(
                title="⬆️ Update Started",
                description=f"**{self.mode_label}** update initiated for **{server_name}**",
                color=discord.Color.green()
            )
            embed.add_field(name="👤 Requested By", value=f"@{username}", inline=True)
            embed.add_field(name="🔧 Update Type", value=self.mode_label, inline=True)
            
            if self.mode in ['full', 'reinit']:
                embed.add_field(
                    name="⏳ Expected Duration", 
                    value="5-15 minutes depending on server size", 
                    inline=False
                )
        else:
            embed = discord.Embed(
                title="❌ Update Failed",
                description=f"Could not start update for **{server_name}**",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Error Details",
                value=response.get('err_code', 'Unknown error'),
                inline=False
            )
        
        await interaction.edit_original_response(embed=embed, view=None)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="❌ Update Cancelled",
            description="Update operation was cancelled by user.",
            color=discord.Color.grey()
        )
        await interaction.response.edit_message(embed=embed, view=None)

class EnhancedEditDescriptionModal(discord.ui.Modal, title='📝 Edit Server Description'):
    def __init__(self, gameuid: str, servername: str):
        super().__init__(title='📝 Edit Server Description')
        self.gameuid = gameuid
        self.servername = servername
        
        self.description_input = discord.ui.TextInput(
            label='New Server Description',
            placeholder='Enter a new description for your server...',
            required=True,
            max_length=200,
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.description_input)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        if 'error' in (result := get_peon_orcs())['status']:
            embed = build_card(status='nok', message="No orchestrators registered")
            await interaction.followup.send(embed=embed)
            return
        
        server_uid = f"{self.gameuid}.{self.servername}"
        orchestrator = result['data'][0]
        
        desc_result = server_update_description(
            orchestrator['url'],
            orchestrator['key'],
            server_uid,
            self.description_input.value
        )
        
        if desc_result['status'] == 'success':
            embed = discord.Embed(
                title="✅ Description Updated",
                description=f"Description for **{server_uid}** has been updated!",
                color=discord.Color.green()
            )
            embed.add_field(
                name="📝 New Description",
                value=f"*{self.description_input.value}*",
                inline=False
            )
        else:
            embed = discord.Embed(
                title="❌ Update Failed",
                description="Could not update server description",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Error Details",
                value=desc_result.get('message', 'Unknown error'),
                inline=False
            )
        
        # Try to replace the original interaction if possible, otherwise send followup
        try:
            await interaction.edit_original_response(embed=embed, view=None)
        except:
            await interaction.followup.send(embed=embed)

class EnhancedDeleteConfirmView(discord.ui.View):
    def __init__(self, gameuid: str, servername: str):
        super().__init__(timeout=60)
        self.gameuid = gameuid
        self.servername = servername
        
    def _disable_all_buttons(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

    @discord.ui.button(label="🗃️ Delete Container Only", style=discord.ButtonStyle.danger, row=0)
    async def delete_container(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._perform_delete(interaction, "destroy", False, "Container Only")

    @discord.ui.button(label="💥 Delete Everything", style=discord.ButtonStyle.danger, row=0) 
    async def delete_everything(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._perform_delete(interaction, "destroy", True, "Complete Deletion")

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.secondary, row=1)
    async def cancel_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._disable_all_buttons()
        embed = discord.Embed(
            title="✅ Deletion Cancelled",
            description="Server deletion was cancelled. Your server is safe!",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=None)

    async def _perform_delete(self, interaction: discord.Interaction, action: str, eradicate: bool, delete_type: str):
        self._disable_all_buttons()
        await interaction.response.edit_message(view=self)
        
        if 'error' in (result := get_peon_orcs())['status']:
            embed = build_card(status='nok', message="No orchestrators registered")
            await interaction.channel.send(embed=embed)
            return
        
        server_uid = f"{self.gameuid}.{self.servername}"
        orchestrator = result['data'][0]
        username = str(interaction.user.display_name)
        
        delete_result = server_delete(
            orchestrator['url'],
            orchestrator['key'],
            server_uid,
            action,
            eradicate
        )
        
        if delete_result['status'] == 'success':
            embed = discord.Embed(
                title=f"💥 Server Deleted - {delete_type}",
                description=f"**{server_uid}** has been removed from the system.",
                color=discord.Color.red()
            )
            embed.add_field(name="👤 Deleted By", value=f"@{username}", inline=True)
            embed.add_field(name="🗑️ Deletion Type", value=delete_type, inline=True)
            
            if not eradicate:
                embed.add_field(
                    name="💾 Data Preserved",
                    value="Player saves and configuration files have been preserved and can be used to recreate the server.",
                    inline=False
                )
            else:
                embed.add_field(
                    name="🚨 Complete Removal",
                    value="ALL server data including saves, configs, and player data has been permanently deleted.",
                    inline=False
                )
        else:
            embed = discord.Embed(
                title="❌ Deletion Failed",
                description=f"Could not delete **{server_uid}**",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Error Details",
                value=delete_result.get('message', 'Unknown error'),
                inline=False
            )
        
        await interaction.edit_original_response(embed=embed, view=None)
