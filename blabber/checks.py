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

async def _can_disconnect(ctx):
    # Count number of users in voice channel excluding context author and bots
    user_count = 0
    for member in ctx.voice_client.channel.members:
        user_count += (not member.bot and member.id != ctx.author.id)

    if user_count > 0:
        try:
            await commands.check_any(
                commands.has_role('Blabby').predicate(ctx), 
                commands.has_permissions(manage_channels=True).predicate(ctx))
        except:
            raise MissingCredentials()


async def _blabber_has_required_permissions(ctx):
    bot = ctx.guild.get_member(ctx.bot.user.id)
    bot_permissions = ctx.author.voice.channel.permissions_for(bot)

    if not bot_permissions.connect:
        raise BlabberMissingConnectPermission(ctx.author.voice.channel.name)
    elif not bot_permissions.speak:
        raise BlabberMissingSpeakPermission(ctx.author.voice.channel.name)


def connect_check():
    async def predicate(ctx):
        if not ctx.author.voice:
            raise NotConnected()
        elif ctx.author.voice is not ctx.voice_client:
            await _blabber_has_required_permissions(ctx)
            await _can_disconnect(ctx)
        return True
    return commands.check(predicate)

def disconnect_check():
    async def predicate(ctx):
        if not ctx.voice_client:
            raise BlabberNotConnected()
        await _can_disconnect(ctx)
        return True
    return commands.check(predicate)

def say_check()
    async def predicate(ctx):
        if ctx.message.content > 600
            raise MessageTooLong()
        return True
    return commands.check(predicate)
