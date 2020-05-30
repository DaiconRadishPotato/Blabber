# roles.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 2/3/2019
# Date last modified: 5/29/2020
# Python Version: 3.8.1
# License: MIT License

from discord import utils, Embed, Colour
from discord.ext import commands

from blabber.checks import *
from blabber.errors import *


class _Roles(commands.Cog):
    """
    Private Permission Cog that allows role managers to give permission for 
    certain users to use blabber

    parameters:
        bot [Bot]: client object representing a Discord bot
    """
    def __init__(self, bot):
        self.prefixes = bot.prefixes

    @commands.command(name="give_blabby", aliases=['gb'])
    @commands.has_permissions(manage_roles=True)
    async def give_blabby(self, ctx, *, user: str=''):
        """
        Gives Blabby role to inputted user, which allows user to have priority
        when using blabber bot commands.

        parameters:
            ctx [Context]: context object produced by a command invocation
            user    [str] (default=''): string object representing a username
                                        or nickname
        """
        # Check if user was provided
        if not user:
            embed = Embed(title=":x: Unable to give Blabby role",
                          description="You must input a user or nickname to "
                          "use this command",
                          colour=Colour.red())
        else:
            # Ensure that user exists
            member = utils.find(
                lambda m: m.name == user or m.nick == user,
                ctx.guild.members)
            await user_is_valid(user, member)

            # Ensure that Blabby role exists
            blabby_role = utils.get(ctx.guild.roles, name="Blabby")
            if not blabby_role:
                blabby = await ctx.guild.create_role(
                    name='Blabby', 
                    reason="To allow certain people to use Blabber Bot.")

            await member.add_roles(blabby_role)

            embed = Embed(title=f":white_check_mark: {user} has been given "
                                 "`Blabby` role",
                          colour=Colour.green())
        await ctx.send(embed=embed)
    
    @give_blabby.error
    async def give_blabby_error(self, ctx, error):
        """
        Local error handler for give_blabby.
        If user parameter is invalid, send an error message.
        If invoker does not have permission to use command, send error message.

        parameters:
            ctx     [Context]: context object produced by a command invocation
            error [Exception]: error object thrown by command function
        """
        if isinstance(error, InvalidUser):
            prefix = self.prefixes[ctx.guild]
            embed = Embed(title=":x: Unable to give Blabby role",
                          description="",
                          colour=Colour.red())
            embed.add_field(name="Input User:",
                            value=f"{error}",
                            inline=False)
            embed.add_field(name="To user give_blabby:",
                            value=f"'{prefix}give_blabby [user/nickname]'",
                            inline=False)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = Embed(title=":x: Unable to give Blabby role",
                          description="`Manage Roles` permission required "
                          "to give `Blabby` role",
                          colour=Colour.red())
        await ctx.send(embed=embed)


def setup(bot):
    """
    Adds private _Roles Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(_Roles(bot))
