# settings.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 4/1/2020
# Python Version: 3.8.1
# License: MIT License

import json

from discord.ext import commands
from discord import Embed, Colour
from blabber.checks import is_guild_owner
from blabber.guild_services import GuildDataService


class Settings(commands.Cog):
    """
    Settings Cog Object that is a collection of commands for managing 
    Blabber's settings for a specific guild.

    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='settings')
    async def settings(self, ctx):
        """
        Displays setting menu for Blabber if no option was passed 
        as a parameter.

        parameter:
            ctx [commands.Context]: discord Contxt object
        """
        if ctx.invoked_subcommand is None:
            prefix = await self._get_prefix(ctx.guild.id)
            embed = Embed(title="Blabber Settings - Menu", 
            description=f"Use the command format `{prefix}settings [option]` "
            "to view more info about an option.",
            colour=Colour.blue())
            embed.add_field(name="Prefix", value=f"`{prefix}settings prefix`")

            await ctx.send(embed=embed)

    @settings.command(name='prefix', aliases=['p'])
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
            MissingRequiredArgument: New prefix was not passed as an argument
        """
        try:
            with open(r"prefixes.json",'r') as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = prefix

            with open(r"prefixes.json",'w') as f:
                json.dump(prefixes, f, indent = 4)
            await ctx.send(f"The new prefix is '{prefix}'")
        except:
            await ctx.send(f"New prefix had trouble setting. "
            "Try again at a later time")

    async def check_prefix(self, bot, message):
        """
        Determines whether a user message is a command by checking if it has a
        specified prefix or @mention

        parameters:
            bot [discord.Bot]: discord Bot object
            message [discord.Message]: the message or context from the guild 
            that called the bot.
        returns:
            prefix: string that is used to call commands from the bot client
        """
        return commands.when_mentioned_or(
            await self._get_prefix(message.guild.id))(bot, message)

    async def _get_prefix(self, guild_id):
        """
        Checks a json file to see if guild has a different prefix 
        and return it.
        Return the original prefix if guild is not in json file.

        raises:
            IOError: raised when file does not exist
        returns:
            prefix: string that is used to call commands from the bot client
        """
        try:
            with open(r"prefixes.json", "r") as f:
                prefixes = json.load(f)
        except:
            return ">"
        
        # Checks if guild from the context exists within json file.
        if str(guild_id) not in prefixes:
            return ">"
        else:
            return prefixes[str(guild_id)]

    @set_prefix.error
    async def set_prefix_error(self, ctx, error):
        """

        """
        # if invoker does not pass a prefix, then send current prefix, show 
        # set_prefix command format, and describe prefix requirement. 
        if isinstance(error, commands.MissingRequiredArgument):
            prefix = await self._get_prefix(ctx.guild.id)

            embed = Embed(title="Blabber Settings - Prefix",
            description="Changes the prefix used to command Blabber bot. You "
            "can also use the bot by @mentioning it instead of using the"
            " prefix.",
            colour=Colour.blue())
            
            embed.add_field(name="Current Prefix:", value=f"`{prefix}`")
            embed.add_field(name="Update Prefix:", 
            value=f"`{prefix}settings prefix [new prefix]`")
            embed.add_field(name="Valid Prefix Reqs:", 
            value=f"`Any text, max 5 characters`")
            await ctx.send(embed=embed)


def setup(bot):
    """
    Adds Settings Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Settings(bot))
    bot.command_prefix=bot.get_cog("Settings").check_prefix
