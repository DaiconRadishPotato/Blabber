# settings.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 5/24/2020
# Python Version: 3.8.1
# License: MIT License

from discord import Embed, Colour
from discord.ext import commands

from blabber.checks import is_guild_owner


class Settings(commands.Cog):
    """
    Settings Cog Object that is a collection of commands for managing
    Blabber's settings for a specific guild.

    parameters:
        bot [discord.Bot]: discord Bot object
    """

    def __init__(self, bot):
        self.prefixes = bot.prefixes

    @commands.group(name='settings')
    async def settings(self, ctx):
        """
        Displays setting menu for Blabber if no option was passed as a
        parameter.

        parameter:
            ctx [Context]: discord Contxt object
        """
        # Check if user invoked a subcommand
        if ctx.invoked_subcommand is None:
            embed = Embed(
                title="Blabber Settings - Menu",
                description="Use the command format `{prefix}settings [option]`"
                "to view more info about an option.",
                colour=Colour.blue())

            # Generate options menu
            prefix = await self._get_prefix(ctx.guild)
            embed.add_field(name="Prefix", value=f"`{prefix}settings prefix`")

            await ctx.send(embed=embed)

    @settings.command(name='prefix', aliases=['p'])
    @commands.check(is_guild_owner)
    async def set_prefix(self, ctx, prefix: str):
        """
        Changes prefix used to invoke Blabber for a particular guild.

        parameter:
            ctx [Context]: discord Contxt object
            prefix [str]: string used before commands to invoke blabber bot
        raises:
            MissingRequiredArgument: New prefix was not passed as an argument
        """
        self.prefixes[ctx.guild] = prefix
        await ctx.send(f":white_check_mark: **The new prefix is **'{prefix}'")

    async def _get_prefix(self, guild):
        """
        Checks cache and database for the guilds prefix.

        parameters:
            guild [Guild]: discord Guild object
        returns:
            str: used to call commands from the bot client
        """
        prefix = self.prefixes[guild]
        return prefix

    async def check_prefix(self, bot, message):
        """
        Determines whether a user message is a command by checking if it has a
        specified prefix or @mention

        parameters:
            bot [Bot]: discord Bot object
            message [Message]: the message or context from the guild that 
                               called the bot.
        returns:
            str: used to call commands from the bot client
        """
        return commands.when_mentioned_or(
            await self._get_prefix(message.guild))(bot, message)

    @set_prefix.error
    async def set_prefix_error(self, ctx, error):
        """
        Sends informational embed if set prefix command is missing arguments.

        parameters:
            ctx [Context]: discord Context object
            error [Error]: general Error object
        """
        # Checks if no paramerter was passed to cause error
        if isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(
                title="Blabber Settings - Prefix",
                description="Changes the prefix used to command Blabber bot. "
                "You can also use the bot by @mentioning it instead of using "
                "the prefix.",
                colour=Colour.blue())

            # Generate prefix information for embed
            prefix = await self._get_prefix(ctx.guild)
            embed.add_field(name="Current Prefix:",
                            value=f"`{prefix}`")
            embed.add_field(name="Update Prefix (max 5 characters):",
                            value=f"`{prefix}settings prefix [new prefix]`")

            await ctx.send(embed=embed)


def setup(bot):
    """
    Adds Settings Cog to bot.
        parameter:
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Settings(bot))
    bot.command_prefix = bot.get_cog("Settings").check_prefix
