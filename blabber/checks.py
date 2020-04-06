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

def bot_can_disconnect():
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
    async def predicate(ctx):
        if not ctx.author.voice:
            raise NotConnected()

        bot = ctx.guild.get_member(ctx.bot.user.id)
        bot_permissions = ctx.author.voice.channel.permissions_for(bot)

        if bot_permissions.connect and bot_permissions.speak:
            return True
        else:
            raise BotMissingVoicePermissions(ctx.author.voice.channel.name)

    return commands.check(predicate)
