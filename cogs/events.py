# events.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/27/2020
# Date last modified: 5/26/2020
# Python Version: 3.8.1
# License: MIT License

import asyncio

from discord import Activity, ActivityType
from discord.ext import commands


class Events(commands.Cog):
    """
    Events Cog that handles events and prints in the python shell.

    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot
    
    async def _change_presence(self, bot):
        """
        Sets up the bot's rich presence when it is online.

        parameter:
            bot [Bot]: discord Bot object
        """
        await bot.wait_until_ready()
        # Checks if bot is not offline every 15 secs
        while not bot.is_closed():
            await bot.change_presence(activity=Activity(
                name=f"@{bot.user.name} help | >help",
                type=ActivityType.listening))
            await asyncio.sleep(15)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Checks the author of the message and sees if they use blabber start.

        parameters:
            message [Message]: discord Message object
        """
        if message.author.id != self.bot.user.id:
            return None
            # await message.channel.send(message.content)
            
    @commands.Cog.listener()
    async def on_ready(self):
        """
        When bot has successfully loaded and online, print out a ready message
        and create a rich presense.
        """
        print(f"{self.bot.user.name} logged in")
        print("------------------")
        self.bot.loop.create_task(self._change_presence(self.bot))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Checks whenever there is a command error and prints information to the 
        guild chat room.

        paramters:
            ctx [Context]: discord Context object
            error [Error]: general Error object
        """
        if isinstance(error, commands.errors.CommandNotFound):
            return

def setup(bot):
    """
    Adds Events Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Events(bot))
