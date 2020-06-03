# roles.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 2/3/2019
# Date last modified: 6/2/2020
# Python Version: 3.8.1
# License: MIT License

from discord import utils, Embed, Colour, Member
from discord.ext import commands

from blabber.checks import *
from blabber.errors import *


class Roles(commands.Cog):
    """
    Collection of commands for managing Guild roles.

    parameters:
        bot [Bot]: client object representing a Discord bot
    """
    def __init__(self, bot):
        self.prefixes = bot.prefixes

    @commands.command(name="giveblabby", aliases=['gb'])
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def giveblabby(self, ctx, *, member_name: str=''):
        """
        Assigns Blabby role to a server member.

        parameters:
            ctx     [Context]: context object produced by a command invocation
            member  [str] (default=''): nickname/username of member in guild
        """
        # Check if member name was provided
        if not member_name:
            embed = Embed(
                title=(":information_source: **No member to assign** `Blabby` "
                       "**role to**"),
                colour=Colour.blue())
        else:
            # Find member in guild
            member = await commands.MemberConverter().convert(ctx, member_name)

            # Ensure that Blabby role exists
            role = utils.get(ctx.guild.roles, name="Blabby")
            if not role:
                role = await ctx.guild.create_role(name='Blabby')

            await member.add_roles(role)

            embed = Embed(
                title=(f":white_check_mark: {member.display_name} has been "
                        "assigned `Blabby` role"),
                colour=Colour.green())
        await ctx.send(embed=embed)
    
    @giveblabby.error
    async def giveblabby_error(self, ctx, error):
        """
        Local error handler for Blabber's giveblabby command.

        parameters:
            ctx     [Context]: context object representing command invocation
            error [Exception]: exception object raised from command function
        """
        embed = Embed(
            title=f":x: **Unable to assign** `Blabby` **role**",
            colour=Colour.red())
        if isinstance(error, commands.BotMissingPermissions):
            embed.description = ("Blabber does not have `Manage Roles` "
                                 "permission")
        elif isinstance(error, commands.MissingPermissions):
            embed.description = ("`Manage Roles` permission required to use "
                                 "this command")
        else:
            member_name = ctx.kwargs['member_name']
            embed.description = f"`{member_name}` was not found in this server"
        await ctx.send(embed=embed)


def setup(bot):
    """
    Adds Roles Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Roles(bot))
