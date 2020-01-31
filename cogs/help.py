# help.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 12/16/2019
# Date last modified: 1/30/2020
# Python Version: 3.8.1
# License: "MIT"

from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = Embed(colour=ctx.author.color)
        embed.set_author(name="Help Directory", icon_url=self.bot.user.avatar_url)
        embed.add_field(name=">help",
                        value="Displays this message.",
                        inline=False)
        embed.add_field(name=">connect or >c",
                        value='Connect Blabber to the voice channel you\'re in',
                        inline=False)
        embed.add_field(name=">disconnect or >dc",
                        value='Disconnect Blabber from its voice channel',
                        inline=False)
        embed.add_field(name=">say [message] or >s [message]",
                        value="Tell Blabber to say something. If Blabber is not in "
                        "the same voice channel, then it will join.",
                        inline=False)
        embed.add_field(name=">prefix [new prefix] or >p [new prefix]",
                        value="Allows the owner of the Server to change the prefix "
                        "for the Blabber Bot commands",
                        inline=False)
        await ctx.send(embed=embed)

        
def setup(bot):
    bot.remove_command('help')
    bot.add_cog(Help(bot))
