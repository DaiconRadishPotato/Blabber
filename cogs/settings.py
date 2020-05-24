# settings.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 5/5/2020
# Python Version: 3.8.1
# License: MIT License

from discord.ext import commands
from discord import Embed, Colour
from blabber.checks import is_guild_owner
from blabber.cache import PrefixCache

class Settings(commands.Cog):
    """
    Settings Cog Object that is a collection of commands for managing
    Blabber's settings for a specific guild.

    parameters:
        bot [discord.Bot]: discord Bot object
    """

    def __init__(self, bot):
        self.bot = bot
        self.prefix_cache = PrefixCache()

    @commands.group(name='settings')
    async def settings(self, ctx):
        """
        Displays setting menu for Blabber if no option was passed as a
        parameter.

        parameter:
            ctx [commands.Context]: discord Contxt object
        """
        if ctx.invoked_subcommand is None:
            prefix = await self._get_prefix(ctx.guild)

            embed = Embed(title="Blabber Settings - Menu",
                          description="Use the command format "
                          f"`{prefix}settings [option]` "
                          "to view more info about an option.",
                          colour=Colour.blue())

            embed.add_field(name="Prefix", value=f"`{prefix}settings prefix`")

            await ctx.send(embed=embed)

    @settings.command(name='prefix', aliases=['p'])
    @commands.check(is_guild_owner)
    async def set_prefix(self, ctx, prefix: str):
        """
        Changes prefix of Blabber for a particular guild. Displays a message
        to user if set was successful or failed.

        parameter:
            ctx [commands.Context]: discord Contxt object
            prefix [str]: string used before commands to invoke blabber bot
        raises:
            MissingRequiredArgument: New prefix was not passed as an argument
        """
        self.prefix_cache[ctx.guild] = prefix
        await ctx.send(f":white_check_mark: **The new prefix is **'{prefix}'")

    async def check_prefix(self, bot, message):
        """
        Determines whether a user message is a command by checking if it has a
        specified prefix or @mention

        parameters:
            bot [discord.Bot]: discord Bot object
            message [discord.Message]: the message or context from the guild
                                       that called the bot.
        returns:
            prefix [str]: that is used to call commands from the bot client
        """
        return commands.when_mentioned_or(
            await self._get_prefix(message.guild))(bot, message)



    async def _get_prefix(self, guild):
        """
        Checks database if guild has a different prefix than the default.
        Returns DEFAULT_PREFIX if record not found on the database

        parameters:
            guild [Guild]: discord Guild object
        returns:
            prefix [str]: that is used to call commands from the bot client
        """
        prefix = self.prefix_cache[guild]
        return prefix


    @set_prefix.error
    async def set_prefix_error(self, ctx, error):
        """
        Sends informational embed to be displayed if set prefix command
        is missing arguments.
        If invoker does not pass a prefix, then send current prefix, show
        set_prefix command format, and describe prefix requirement.

        parameters:
            ctx [commands.Context]: discord Context object
            error [Error]: general Error object
        """

        if isinstance(error, commands.MissingRequiredArgument):
            prefix = await self._get_prefix(ctx.guild)

            embed = Embed(
                title="Blabber Settings - Prefix",
                description="Changes the prefix used to command Blabber bot. "
                "You can also use the bot by @mentioning it instead of using "
                "the prefix.",
                colour=Colour.blue())

            embed.add_field(name="Current Prefix:",
                            value=f"`{prefix}`")

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
    bot.command_prefix = bot.get_cog("Settings").check_prefix
