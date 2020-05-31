# settings.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 5/31/2020
# Python Version: 3.8.1
# License: MIT License

from discord import Embed, Colour
from discord.ext import commands

from blabber.checks import *


class Settings(commands.Cog):
    """
    Collection of commands for managing Blabber guild settings.

    parameters:
        bot [Bot]: client object representing a Discord bot
    """
    def __init__(self, bot):
        self.prefixes = bot.prefixes

    @commands.group(name='settings', aliases=['set'])
    async def settings(self, ctx):
        """
        Displays guild settings commands for Blabber.

        parameters:
            ctx [Context]: context object representing command invocation
        """
        # Check if user invoked a subcommand
        if not ctx.invoked_subcommand:
            prefix = self.prefixes[ctx.guild]
            embed = Embed(
                title=":gear: Server Settings",
                description=(f":information_source: **Use** `{prefix}settings "
                              "[Option]` **to see more options**"),
                colour=Colour.blue())
            embed.add_field(
                name="**Prefix:**",
                value=f"`{prefix}settings prefix`")

            await ctx.send(embed=embed)

    @settings.command(name='prefix', aliases=['p'])
    async def settings_prefix(self, ctx, prefix: str=''):
        """
        Modifies/displays prefix of a particular guild.

        parameter:
            ctx [Context]: context object representing command invocation
            prefix  [str] (default=''): new prefix for a particular guild
        """

        # Check if a prefix was provided
        if not prefix:
            # Retrieve current guild prefix
            prefix = self.prefixes[ctx.guild]

            embed = Embed(
                title=":gear: Prefix Settings",
                description="Changes the prefix for the server",
                colour=Colour.gold())
            embed.add_field(
                name="**Current Prefix:**",
                value=f"`{prefix}`",
                inline=False)

            embed.add_field(
                name="**Update Prefix (max 5 characters):**",
                value=f"`{prefix}settings prefix [New Prefix]`",
                inline=False)

        elif await prefix_is_valid(prefix):
            # Set the new guild prefix
            self.prefixes[ctx.guild] = prefix
            embed = Embed(
                title=( ":white_check_mark: **New server prefix is** "
                       f"`{prefix}`"),
                colour=Colour.green())
        
        await ctx.send(embed=embed)

    @settings_prefix.error
    async def settings_prefix_error(self, ctx, error):
        """
        Local error handler for Blabber's settings prefix command.

        parameters:
            ctx     [Context]: context object representing command invocation
            error [Exception]: exception object raised from command function
        """
        prefix = self.prefixes[ctx.guild]
        embed = Embed(
            title=":x: **Unable to change prefix**",
            description=(f"{error}\n\n:wrench: **Ensure prefix is less "
                          "than** `5`  **characters**"),
            colour=Colour.red())
        await ctx.send(embed=embed)


def setup(bot):
    """
    Adds Settings Cog to bot.

    parameter:
        bot [Bot]: client object representing a Discord bot
    """
    bot.add_cog(Settings(bot))
