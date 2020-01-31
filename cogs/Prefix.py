# prefix.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 12/16/2019
# Date last modified: 1/30/2020
# Python Version: 3.8.1
# License: "MIT"

from discord.ext import commands
import json

async def is_guild_owner(ctx):
    return ctx.author.id == ctx.guild.owner.id    
                         
class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prefix', aliases=['p'])
    @commands.check(is_guild_owner)
    async def prefix(self, ctx, *, prefix):
        with open(r"C:\Users\Jacky's Thinkpad\Desktop\Blabber\src\prefixes.json",'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix
        await ctx.send(f"New prefix is '{prefix}'")

        with open(r"C:\Users\Jacky's Thinkpad\Desktop\Blabber\src\prefixes.json",'w') as f:
            json.dump(prefixes, f, indent = 4)


def setup(bot):
    bot.add_cog(Prefix(bot))
