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

def is_connected():
    async def predicate(ctx):
        if ctx.author.voice:
            return True
        else:
            raise NotConnected()
    return commands.check(predicate)

def bot_is_connected():
    async def predicate(ctx):
        if ctx.voice_client:
            return True
        else:
            raise BotNotConnected()
    return commands.check(predicate)

def bot_can_disconnect():
    async def predicate(ctx):
        await bot_is_connected().predicate(ctx)

        # Count number of users in voice channel excluding context author and bots
        user_count = 0
        for member in ctx.voice_client.channel.members:
            user_count += (not member.bot and member.id != ctx.author.id)

        if user_count == 0:
            return True

        try:
            await commands.has_role('Blabby').predicate(ctx)
            await commands.has_permissions(manage_channels=True).predicate(ctx)
        except:
            raise MissingCredentials()
        else:
            return True

    return commands.check(predicate)

def bot_can_connect():
    async def predicate(ctx):
        await is_connected().predicate(ctx)

        bot = ctx.guild.get_member(ctx.bot.user.id)
        bot_permissions = ctx.author.voice.channel.permissions_for(bot)

        if bot_permissions.connect and bot_permissions.speak:
            return True
        else:
            raise BotMissingVoiceChannelPermissions(ctx.author.voice.channel.name)

    return commands.check(predicate)

def bot_can_move():
    async def predicate(ctx):
        await is_connected().predicate(ctx)

        try:
            await bot_can_connect().predicate(ctx)
            await bot_can_disconnect().predicate(ctx)
        except BotMissingVoiceChannelPermissions as e:
            raise e
        except:
            raise BotConnectedToAnotherChannel()
        else:
            return True

    return commands.check(predicate) 
