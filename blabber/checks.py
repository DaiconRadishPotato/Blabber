# checks.py
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 3/9/2020
# Date last modified: 3/9/2020
# Python Version: 3.8.1
# License: "MIT"

from discord.ext import commands

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
