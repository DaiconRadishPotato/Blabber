# profiles.py
#
# Author: Fanny Avila (Fa-Avila)
# Contributor:  Jacky Zhang (jackyeightzhang),
#               Marcos Avila (DaiconV)
# Date created: 3/27/2020
# Date last modified: 5/31/2020
# Python Version: 3.8.1
# License: MIT License

from discord import Embed, Colour
from discord.ext import commands

from blabber.checks import *


class Profiles(commands.Cog):
    """
    Collection of commands for managing Blabber user settings.

    parameters:
        bot [Bot]: client object representing a Discord bot
    """
    def __init__(self, bot):
        self.voice_profiles = bot.voice_profiles
        self.prefixes = bot.prefixes

    @commands.command(name='voice', aliases=['v'])
    async def voice(self, ctx, *, alias: str=''):
        """
        Modifies/displays voice profile information of the command invoker.

        parameter:
            ctx [Context]: context object representing command invocation
            alias   [str] (default=''): name of command invoker's new voice
        """
        member = ctx.author.display_name

        # Check if an alias was provided
        if not alias:
            # Retrieve command invoker's current alias
            alias = self.voice_profiles[(ctx.author, ctx.channel)]

            prefix = self.prefixes[ctx.guild]
            embed = Embed(
                title=":gear: **Voice Settings**",
                colour=Colour.gold())
            embed.add_field(
                name=f"**{member}'s Current Voice:**",
                value=f"`{alias}`",
                inline=False)
            embed.add_field(
                name="**Update Voice:**",
                value=f"`{prefix}voice [New Voice]`",
                inline=False)
        elif await voice_is_valid(alias):
            # Set the command invoker's new alias
            self.voice_profiles[(ctx.author, ctx.channel)] = alias
            embed = Embed(
                title=(f":white_check_mark: **{member}'s new voice is **"
                       f"`{alias}`"),
                colour=Colour.green())

        await ctx.send(embed=embed)

    @voice.error
    async def voice_error(self, ctx, error):
        """
        Local error handler for Blabber's voice command.

        parameters:
            ctx     [Context]: context object representing command invocation
            error [Exception]: exception object raised from command function
        """
        prefix = self.prefixes[ctx.guild]
        embed = Embed(
            title=":x: **Unable to set voice**",
            description=(f"{error}\n\n:wrench: **Use the** `>list` "
                          "**command to search for supported voices**"),
            colour=Colour.red())
        await ctx.send(embed=embed)


def setup(bot):
    """
    Adds Profiles Cog to bot.

    parameter:
        bot [Bot]: client object representing a Discord bot
    """
    bot.add_cog(Profiles(bot))
