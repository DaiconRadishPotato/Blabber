# checks.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 3/9/2020
# Date last modified: 3/9/2020
# Python Version: 3.8.1
# License: "MIT"

import discord
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


def has_role(ctx, role):
    return discord.utils.get(ctx.author.roles, name=role) != None

def has_permission(ctx, permission):
    return getattr(ctx.author.permissions_in(ctx.channel), permission, False)
