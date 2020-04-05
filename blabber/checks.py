# checks.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 3/9/2020
# Date last modified: 3/9/2020
# Python Version: 3.8.1
# License: MIT License

from discord.ext import commands

from blabber.errors import *

def is_guild_owner(ctx):
    """
    Checks if invoker is the owner of the guild.

    parameter:
        ctx [commands.Context]: discord Context object
    returns:
        boolean: True if invoker is owner of guild
    """
    return ctx.author == ctx.guild.owner

def can_disconnect_bot():
    async def predicate(ctx):
        blabby = commands.has_role('Blabby').predicate
        manage_channels = commands.has_permissions(manage_channels=True).predicate
        if not ctx.voice_client:
            raise BotNotConnected()

        # Count number of users in voice channel excluding context author and bots
        user_count = 0
        for member in ctx.voice_client.channel.members:
            user_count += (not member.bot and member.id != ctx.author.id)

        try:
            return user_count == 0 or await blabby(ctx) or await manage_channels(ctx)
        except (commands.MissingRole, commands.MissingPermissions):
            raise MissingCredentials() 

    return commands.check(predicate)

def bot_can_connect():
    pass
