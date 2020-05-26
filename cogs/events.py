# events.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 1/27/2020
# Date last modified: 3/4/2020
# Python Version: 3.8.1
# License: MIT License

import asyncio

from discord import Activity, ActivityType
from discord.ext import commands


async def change_presence(bot):    
    """
    Sets up the bot's rich presence when it is online.
    Sets its rich presence to a ready and waiting message.
    Checks every 15 seconds in the background if bot is in use.
    If so, then the rich presence does not change.
    If not, rich presence message is changed back to ready and waiting.

    parameter:
        bot [discord.Bot]: discord Bot object
    """
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=Activity(
            name=f"@{bot.user.name} help | >help",
            type=ActivityType.listening))
        await asyncio.sleep(15)

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

        parameters:
            message [discord.Message]: discord Message object
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
        self.bot.loop.create_task(change_presence(self.bot))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Checks whenever there is a command error and prints information to the 
        guild chat room.
        If command does not exist, let user know in chat and what the bot saw as
        input.
        If error is something else, let the user know for debugging purposes.

        paramters:
            ctx [commands.Context]: discord Context object
            error [Error]: general Error object
        """
        if isinstance(error, commands.errors.CommandNotFound):
            None

def setup(bot):
    """
    Adds Events Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Events(bot))
