# checks.py
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 3/9/2020
# Date last modified: 3/9/2020
# Python Version: 3.8.1
# License: "MIT"

from discord.ext import commands

from blabber.errors import *

@commands.check
async def is_guild_owner(ctx):
    """
    Checks if invoker is the owner of the guild.

    parameter:
        ctx [commands.Context]: discord Context object
    returns:
        boolean: True if invoker is owner of guild
    """
    return ctx.author == ctx.guild.owner

@commands.check
async def is_bot_alone(ctx):
    """
    Checks if bot is not in use.

    parameter:
        ctx [commands.Context]: discord Context object
    returns:
        boolean: True if bot is not connect, bot is alone, bot is with inovker
        and no one else.
    """
    return ctx.voice_client == None or \
        len(ctx.voice_client.channel.members) == 1 or \
            (len(ctx.voice_client.channel.members) == 2 and \
                ctx.author.voice.channel == ctx.voice_client.channel)

async def is_connected(ctx):
    if not ctx.author.voice:
        raise NotConnected()
    return True


async def blabber_has_required_permissions(ctx):
    bot = ctx.guild.get_member(ctx.bot.user.id)
    bot_permissions = ctx.author.voice.channel.permissions_for(bot)

    if not bot_permissions.connect:
        raise BlabberMissingConnectPermission(ctx.author.voice.channel.name)
    elif not bot_permissions.speak:
        raise BlabberMissingSpeakPermission(ctx.author.voice.channel.name)

    return True

async def can_disconnect(ctx):
    # Count number of users in voice channel excluding context author and bots
    user_count = 0
    for member in ctx.voice_client.channel.members:
        user_count += (not member.bot and member.id != ctx.author.id)

    if user_count > 0:
        try:
            await commands.has_role('Blabby').predicate(ctx)
            await commands.has_permissions(manage_channels=True).predicate(ctx)
        except:
            raise MissingCredentials()


async def can_move(ctx):
    await can_disconnect(ctx)
    await blabber_has_required_permissions(ctx)
    return True
