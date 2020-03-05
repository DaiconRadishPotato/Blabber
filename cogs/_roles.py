# _roles.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 2/3/2019
# Date last modified: 3/4/2020
# Python Version: 3.8.1
# License: "MIT"

from discord.ext import commands
import json
import asyncio

class _Roles(commands.Cog):
    """
    Private Permission Cog that allows role managers to give permission for 
    certain users to use blabber
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="give_blabby", aliases=['gb'])
    @commands.has_permissions(manage_roles=True)
    async def give_permission(self, ctx, user: str):
        """
        Creates Blabby role if it does not already exist in guild.
        Gives Blabby role to inputted user, which allows user to invoke blabber
        bot commands.

        parameters:
            ctx [commands.Context]: discord Context object
            user [str]: username or nickname of user
        """
        if user == '':
            await ctx.send("Blabber::Roles you need to include a "
                           "username/nickname as a parameter")
            return
        #discord utils get to get blabby role
        role_blabby = next((role for role in await ctx.guild.fetch_roles()
                  if "Blabby" == str(role)), None)
        if(blabby is None):
            blabby = await ctx.guild.create_role(name='Blabby', reason="To allow certain"
                                 " people to use Blabber Bot.")
            await ctx.send("Blabber::Roles Created Blabby role "
                           "for users of Blabber")
        member = ctx.guild.get_member_named(user)
        if (member is None):
            await ctx.send(f"Blabber::Roles User {user} doesn't exist")
            return
        await member.add_roles(blabby)
        await ctx.send(f"Blabber::Roles User {user} has Blabby now")

def setup(bot):
    """
    Adds private _Roles Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(_Roles(bot))
