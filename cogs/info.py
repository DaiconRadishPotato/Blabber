# info.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/30/2020
# Date last modified: 3/24/2020
# Python Version: 3.8.1
# License: MIT License

from discord.ext import commands
from discord import Embed

class Info(commands.Cog):
    """
    Collection of commands for displaying information about Blabber for each 
    guild.

    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['h'])
    async def help(self, ctx):
        """
        Prints out description of all available commands for Blabber to the 
        text channel where the bot was invoked.

        paramters:
            ctx [commands.Context]: discord Context object
        """
        embed = Embed(colour=ctx.author.color)
        embed.set_author(name="Help Directory", 
        icon_url=self.bot.user.avatar_url)

        embed.add_field(name=f"{ctx.prefix}help",
        value="Displays this message.",
        inline=False)

        embed.add_field(name=f"{ctx.prefix}connect or {ctx.prefix}c",
        value='Connect Blabber to the voice channel you\'re in',
        inline=False)
        
        embed.add_field(name=f"{ctx.prefix}disconnect or {ctx.prefix}dc",
        value='Disconnect Blabber from its voice channel',
        inline=False)

        embed.add_field(name=f"{ctx.prefix}say [message] or {ctx.prefix}s "
        "[message]",
        value="Tell Blabber to say something. If Blabber is not in the same "
        "voice channel, then it will join.",
        inline=False)

        embed.add_field(name=f"{ctx.prefix}set_prefix [new prefix] or "
        f"{ctx.prefix}sp [new prefix]", 
        value="Allows the owner of the Server to change the prefix for the "
        "Blabber Bot commands",
        inline=False)

        embed.add_field(name=f"{ctx.prefix}get_prefix or {ctx.prefix}gp", 
        value="Allows users to see the prefix for the the servers Blabber Bot 
        "commands",
        inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    """
    Removes templated help function and adds Help Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Info(bot))
