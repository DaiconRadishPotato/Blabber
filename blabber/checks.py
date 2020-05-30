# checks.py
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 3/9/2020
# Date last modified: 5/29/2020
# Python Version: 3.8.1
# License: MIT License

from discord.ext import commands

from blabber import supported_voices, supported_genders, supported_languages
from blabber.errors import *


async def is_guild_owner(ctx):
    """
    Checks if invoker is the owner of the guild.

    parameter:
        ctx [commands.Context]: discord Context object
    returns:
        boolean: True if invoker is owner of guild
    """
    return ctx.author == ctx.guild.owner


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
            await commands.has_permissions(manage_channels=True).predicate(ctx)
        except:
            try:
                await commands.has_role('Blabby').predicate(ctx)
            except:
                raise MissingCredentials()


async def tts_message_is_valid(message):
    if len(message) > 600:
        raise TTSMessageTooLong()
    return True


async def voice_is_valid(alias):
    if alias not in supported_voices:
        raise VoiceNotSupported(alias)
    return True


async def gender_is_valid(gender):
    if not any(g == gender for g in supported_genders):
        raise GenderNotSupported(gender)
    return True


async def language_is_valid(language):
    if language not in supported_languages:
        raise LanguageNotSupported(language)
    return True


async def prefix_is_valid(prefix):
    if len(prefix) > 5:
        raise InvalidPrefix(prefix)
    return True


async def user_is_valid(user, member):
    if not member:
        raise InvalidUser(user)
    return True