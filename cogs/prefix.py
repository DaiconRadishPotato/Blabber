# prefix.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 1/30/2020
# Date last modified: 1/19/2020
# Python Version: 3.8.1
# License: "MIT"

from discord.ext import commands
import json

async def is_guild_owner(ctx):
    """
    Checks if invoker is the owner of the guild.

    parameter:
        ctx [commands.Context]: discord Context object
    returns:
        boolean
    """
    return ctx.author.id == ctx.guild.owner.id  
                         
class Prefix(commands.Cog):
    """
    Prefix Cog Object used to alter the guild's blabber bot prefix

    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prefix', aliases=['p'])
    @commands.check(is_guild_owner)
    async def prefix(self, ctx, *, prefix):
        """
        Changes prefix of blabber bot for a particular guild.

        parameter:
            ctx [commands.Context]: discord Contxt object
            prefix [str]: string used before command names to invoke blabber bot
        """
        with open(r"prefixes.json",'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix
        await ctx.send(f"New prefix is '{prefix}'")

        with open(r"prefixes.json",'w') as f:
            json.dump(prefixes, f, indent = 4)


def setup(bot):
    """
    Adds Prefix Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Prefix(bot))
