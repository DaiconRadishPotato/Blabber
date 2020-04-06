# profiles.py
#
# Author: Fanny Avila (Fa-Avila)
# Contributor:  Jacky Zhang (jackyeightzhang),
#               Marcos Avila (DaiconV)
# Date created: 3/27/2020
# Date last modified: 3/30/2020
# Python Version: 3.8.1
# License: MIT License

from discord.ext import commands
from blabber.checks import is_guild_owner
#>>>added
from blabber.user_services import UserDataService
from blabber.guild_services import GuildDataService

class Profiles(commands.Cog):
    """
    Settings Cog Object that is a collection of commands for managing 
    Blabber's settings for a specific guild

    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='set_voice', aliases=['sv'])
    async def set_voice(self, ctx, *, voice=''):
        """
        Sets up and updates a user voice profile.

        parameter:
            ctx [commands.Context]: discord Contxt object
            voice [str]: string representing a specific voice
        """
        try:
          uds = UserDataService()    
          if uds.is_valid_voice(voice)==1:
            print(f'{ctx.author.id} , {ctx.author.name}, {ctx.channel.id}')
            uds.add_user(ctx.author.id, ctx.author.name)
            uds.set_voice(ctx.author.id, ctx.channel.id, voice)
            await ctx.send(f"The new voice is '{voice}'")
          else:
            await ctx.send(f"Had trouble setting up the new voice.",
            "'{voice}' is not a valid voice.")
        except:
          await ctx.send(f"Had trouble setting up the new voice.")
          
    @commands.command(name='get_voice', aliases=['gv'])
    async def get_voice(self, ctx):
        """
        Prints current users current voice profile.

        parameter:
            ctx [commands.Context]: discord Contxt object
        """
        try:
          uds = UserDataService()
          voice = uds.get_voice(ctx.author.id, ctx.channel.id)
          await ctx.send(f"The current voice is: '{voice[0]}'")
        except:
          await ctx.send("Having trouble getting your voice profile")
          
def setup(bot):
    """
    Adds Settings Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Profiles(bot))