# roles.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 2/3/2019
# Date last modified: 5/24/2020
# Python Version: 3.8.1
# License: MIT License

import discord

from discord.ext import commands


class _Roles(commands.Cog):
    """
    Private Permission Cog that allows role managers to give permission for 
    certain users to use blabber
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="give_blabby", aliases=['gb'])
    @commands.has_permissions(manage_roles=True)
    async def give_blabby(self, ctx, *,user: str):
        """
        Gives Blabby role to inputted user, which allows user to invoke blabber
        bot commands.

        parameters:
            ctx [commands.Context]: discord Context object
            user [str]: username or nickname of user
        raises:
            MissingRequiredArgument: raised when no user is given
            AttributeError: raised when user or blabby role does not exist 
        """
        blabby_role = discord.utils.get(ctx.guild.roles, name="Blabby")
        member = ctx.guild.get_member_named(user)
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
        # If user arguement was not passed to the command, warn invoker of this
        # parameter requirement
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Roles::give_blabby You need to include a username/"
            "nickname as a parameter to assign the \"blabby\" role to someone")
        elif isinstance(error.original, AttributeError):
            # If user does not exist, warns invoker that the user does not
            # exist or that they have mispelled the name.
            if(discord.utils.get(ctx.guild.roles, name="Blabby") is not None):
                await ctx.send(f"Roles::give_blabby User {ctx.args[2]} does not"
                " exist")
            # If Blabby role does not exist, creates Blabby role for guild and
            # adds role to invoker
            else:
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
