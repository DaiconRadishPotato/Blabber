# events.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 12/16/2019
# Date last modified: 1/27/2020
# Python Version: 3.8.1
# License: "MIT"

from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            await ctx.send('Blabber::on_command_error '
                           f'"{ctx.message.content}" '
                           'is not a command for Blabber.')
        else:
            await ctx.send(error)


def setup(bot):
    bot.add_cog(Events(bot))
