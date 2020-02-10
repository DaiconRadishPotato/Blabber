# _permission.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 2/3/2019
# Date last modified: 2/6/2020
# Python Version: 3.8.1
# License: "MIT"

from discord.ext import commands
import json
import asyncio

async def is_guild_owner(ctx):
    return ctx.author.id == ctx.guild.owner.id

class _Permission(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="give_blabby", aliases=['gb'])
    @commands.has_permissions(manage_roles=True)
    async def give_permission(self, ctx, user: str):
        if(len(user) == 0):
            await ctx.send("Blabber::Permissions you need to include a "
                           "username/nickname as a parameter")
            return
        blabby = next((role for role in await ctx.guild.fetch_roles()
                  if "Blabby" == str(role)), None)
        if(blabby is None):
            blabby = await ctx.guild.create_role(name='Blabby', reason="To allow certain"
                                 " people to use Blabber Bot.")
            await ctx.send("Blabber::Permissions Created Blabby role "
                           "for users of Blabber")
        member = ctx.guild.get_member_named(user)
        if (member is None):
            await ctx.send(f"Blabber::Permissions User {user} doesn't exist")
            return
        await member.add_roles(blabby)
        await ctx.send(f"Blabber::Permissions User {user} has Blabby now")

def setup(bot):
    bot.add_cog(_Permission(bot))
