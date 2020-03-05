# errors.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 2/26/2020
# Date last modified: 3/4/2020
# Python Version: 3.8.1
# License: "MIT"

from discord.ext import commands


class Errors(commands.Cog):
    """
    Errors Cog that handles unexpected erros and prints in the python shell.

    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot

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
            await ctx.send('Blabber::on_command_error '
                           f'"{ctx.message.content}" '
                           'is not a command for Blabber.')
        # else:
        #     await ctx.send(error)
        #     raise error


def setup(bot):
    """
    Adds Errors Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Errors(bot))
