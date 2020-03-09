# settings.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 3/9/2020
# Python Version: 3.8.1
# License: MIT License

from discord.ext import commands
from blabber.checks import is_guild_owner

import json 


class Settings(commands.Cog):
    """
    Settings Cog Object that is a collection of commands for managing 
    Blabber's settings for a specific guild

    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='prefix', aliases=['p'])
    @commands.check(is_guild_owner)
    async def prefix(self, ctx, *, prefix):
        """
        Changes prefix of Blabber for a particular guild.

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
    Adds Settings Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Settings(bot))
