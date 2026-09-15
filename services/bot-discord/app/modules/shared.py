import logging
import sys
import requests
import os
import re
import discord
from . import *
from .orchestrator import get_peon_orcs, get_orchestrator_details, get_orchestrator_details_async


def parse_server_channel_name(channel_name):
    """Split a server channel into (game_uid, servername) while preserving hyphenated server names."""
    if not channel_name or not isinstance(channel_name, str):
        return None

    channel_name = channel_name.strip()
    if not channel_name or channel_name == settings.get('control_channel'):
        return None

    parts = channel_name.split('-')
    if len(parts) < 2:
        return None

    return parts[0], '-'.join(parts[1:])


def identify_channel(channel_request,args=tuple()):
    if channel_request == settings['control_channel']:
        permission='admin'
        logging.debug(f" <control channel> - {settings['control_channel']}")
    else:
        permission='user'
        logging.debug(f" <request channel> - {settings['control_channel']}")
        if args:
            args = tuple(channel_request.split('-'))[::-1] + args
        else:
            args = tuple(channel_request.split('-'))[::-1]
    args = (permission,) + args
    return args

def build_card(status='err', message="*HEY DEV, SOMETHING WENT WRONG BUT PEON NEED SOMETHING TO SAY!!!*", title=None):
    if status == 'ok':
        embed = discord.Embed(title=title, description=f"{message}", color=discord.Color.blue())
    elif status == 'nok':
        embed = discord.Embed(title=title, description=f"{message}", color=discord.Color.orange())
    elif status == 'err':
        embed = discord.Embed(title=title, description=f"{message}", color=discord.Color.red())
    else:
        embed = discord.Embed(title=title, description=f"{message}")
    return embed

async def build_about_card():
    about_path = os.path.join(REFERENCE_DIR, settings['language'], "about.md")
    with open(about_path, "r") as file:
        response = file.read()
    response = response.replace('[BOT_VERSION]',os.environ.get('VERSION', '-.-.-'))
    if (orchestrators := get_peon_orcs())['status'] == "success":
        if orchestrators['data']:
            orcstring = ""
            for orc in orchestrators['data']:
                if (orc_response := await get_orchestrator_details_async(url=orc['url'],api_key=orc['key']))['status'] == "success":
                    info = orc_response['data']
                    orcstring += f"- Orchestrator: {orc['name']} [{info['version']}](<https://docs.warcamp.org/development/50_bot_discord/#release-notes>)\n"
                else:
                    orcstring += f"- Orchestrator: {orc['name']} [UNKNOWN](<https://docs.warcamp.org/development/50_bot_discord/#release-notes>)\n"
            response = response.replace('[ORCHESTRATORS]',f"{orcstring}")
    try:
        file_contents = requests.get(games_url, timeout=10).text
        servers = "### Supported Games\nBelow is a list of games that are currently supported by the PEON Project.\n"
        for line in file_contents.splitlines():
            if re.search(r'- \[x\]', line):
                line = re.sub(r'- \[x\]', '- ', line)
                line = re.sub('./guides/games/', 'https://docs.warcamp.org/guides/games/', line)
                line = re.sub('.md', '', line)
                servers += line + '\n'
    except:
        servers = ""
    response = response.replace('[GAME_SERVERS]',servers)
    embed = discord.Embed(description=response)
    embed.set_image(url=bot_image) 
    return embed

async def remove_interactions(interaction, keep=0, message_prefix=None):
        channel = interaction.channel
        logging.debug("Cleaning channel")
        async for message in channel.history(limit=50):
            if ((str(message.author)).split('#')[0] == interaction.client.user.name and message.embeds) and (message.id != keep):
                first_embed = message.embeds[0]
                if first_embed.image and first_embed.image.url and first_embed.image.url == bot_image:
                    await message.delete()
                elif first_embed.thumbnail and first_embed.thumbnail.url == bot_thumbnail:
                    await message.delete()
                elif first_embed.color == discord.Color.yellow():
                    await message.delete()
                elif message_prefix:
                    if message.content.startswith(message_prefix):
                        await message.delete()

async def replace_interaction_with_result(interaction: discord.Interaction, result_embed: discord.Embed, ephemeral: bool = False):
    """Replace an interactive message with a simple result message"""
    try:
        # Edit the original message to remove all interactions and show result
        await interaction.edit_original_response(embed=result_embed, view=None)
    except:
        # Fallback: send a followup if editing fails
        await interaction.followup.send(embed=result_embed, ephemeral=ephemeral)
    
    # Clean up any related messages
    await remove_interactions(interaction)