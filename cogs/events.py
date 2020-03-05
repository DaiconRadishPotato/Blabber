# events.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 1/27/2020
# Date last modified: 2/18/2020
# Python Version: 3.8.1
# License: "MIT"

from discord.ext import commands


class Events(commands.Cog):
    """
    Events Cog that handles events prints in the python shell.

    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Checks the author of the message and sees if they use blabber start.
        """
        if message.author == self.bot:
            return


def setup(bot):
    """
    Adds Events Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Events(bot))
