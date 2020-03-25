# settings.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 3/24/2020
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

    @commands.command(name='set_prefix', aliases=['sp'])
    @commands.check(is_guild_owner)
    async def set_prefix(self, ctx, *, prefix):
        """
        Changes prefix of Blabber for a particular guild.

        parameter:
            ctx [commands.Context]: discord Contxt object
            prefix [str]: string used before command names to 
            invoke blabber bot
        raises:
            IOError: raised when file does not exist
        """
        try:
            with open(r"prefixes.json",'r') as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = prefix

            with open(r"prefixes.json",'w') as f:
                json.dump(prefixes, f, indent = 4)
            await ctx.send(f"The new prefix is '{prefix}'")
        except:
            await ctx.send(f"New prefix had trouble setting. Try again at a "
            "later time")
    
    @commands.command(name='get_prefix', aliases=['gp'])
    async def get_prefix(self, ctx):
        """
        Prints current prefix for blabber commands for a particular guild.

        parameter:
            ctx [commands.Context]: discord Contxt object
        raises:
            IOError: raised when file does not exist
        """
        try:
            with open(r"prefixes.json", "r") as f:
                prefixes = json.load(f)
            # Checks if guild from the context exists within json file.
            if str(ctx.guild.id) not in prefixes:
                await ctx.send("The current prefix is: \">\"")
        except:
            await ctx.send("The current prefix is: \">\"")

        prefix = prefixes[str(ctx.guild.id)]
        await ctx.send("The current prefix is: \"" + prefix + "\"")

    async def check_prefix(self, bot, message):
        """
        Checks a json file to see if guild has a different prefix 
        and return it.
        Return the original prefix if guild is not in json file.

        parameters:
            bot [discord.Bot]: discord Bot object
            message [discord.Message]: the message or context from the guild 
            that called the bot.
        raises:
            IOError: raised when file does not exist
        returns:
            prefix: string that is used to call commands from the bot client
        """
        try:
            with open(r"prefixes.json", "r") as f:
                prefixes = json.load(f)
            # Checks if guild from the context exists within json file.
            if str(message.guild.id) not in prefixes:
                return commands.when_mentioned_or(">")(bot, message)
        except:
            return commands.when_mentioned_or(">")(bot, message)

        prefix = prefixes[str(message.guild.id)]
        return commands.when_mentioned_or(prefix)(bot, message)


def setup(bot):
    """
    Adds Settings Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Settings(bot))
    bot.command_prefix=bot.get_cog("Settings").check_prefix
