# roles.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 2/3/2019
# Date last modified: 5/28/2020
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
    """
    def __init__(self, bot):
        self.prefixes = bot.prefixes

    @commands.command(name="give_blabby", aliases=['gb'])
    @commands.has_permissions(manage_roles=True)
    async def give_blabby(self, ctx, *, user: str=''):
        """
        Gives Blabby role to inputted user, which allows user to invoke blabber
        bot commands.

        parameters:
            ctx [commands.Context]: discord Context object
            user [str]: username or nickname of user
        raises:
            AttributeError: raised when user or blabby role does not exist 
        """
        # Check if user was provided
        if not user:
            embed = Embed(title=":x: Unable to give Blabby role",
                          description="You must input a user or nickname to "
                          "use this command",
                          colour=Colour.red())
            await ctx.send(embed=embed)
        else:
            # Ensure that user exists
            member = ctx.guild.get_member(user)
            await user_is_valid(user, member)

            blabby_role = utils.get(ctx.guild.roles, name="Blabby")
            await member.add_roles(blabby_role)
            await ctx.send(f"Blabber::Roles User {user} has Blabby now")
    
    @give_blabby.error
    async def give_blabby_error(self, ctx, error):
        """
        Local On_Error Function for give_blabby

        parameters:
            ctx [commands.Context]: discord Context object
            error [commands.CommandError]: discord Command Error object
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
            await ctx.send(embed=embed)
        elif not utils.get(ctx.guild.roles, name="Blabby"):
            blabby = await ctx.guild.create_role(name='Blabby', reason="To "
            "allow certain people to use Blabber Bot.")
            await ctx.send("Roles::give_blabby Created Blabby role for "
            "users of Blabber")
            await self.give_blabby(ctx, ctx.args[2])


def setup(bot):
    """
    Adds private _Roles Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(_Roles(bot))
