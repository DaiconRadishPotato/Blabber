# profiles.py
#
# Author: Fanny Avila (Fa-Avila)
# Contributor:  Jacky Zhang (jackyeightzhang),
#               Marcos Avila (DaiconV)
# Date created: 3/27/2020
# Date last modified: 3/30/2020
# Python Version: 3.8.1
# License: MIT License

import json
from discord.ext import commands
from discord import Embed, Colour
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
        self.default_voice=('voice_1', 'de-DE-Standard-F', 'FEMALE', 'de', 'de-DE')
        self.aliases=set()
        with open(r'./blabber/voices.json', 'r') as f:
            voice_dict=json.load(f)
            for voice in voice_dict['voices']:
                self.aliases.add(voice['alias'])
                
    @commands.command(name='set_voice', aliases=['sv'])
    async def set_voice(self, ctx, *, voice):
        """
        Sets up and updates a user voice profile.
        
        parameter:
            ctx [commands.Context]: discord Contxt object
            voice [str]: string representing a specific voice
        """
        voice=voice.lower()
        try:
            if voice is 'default':
                await ctx.send(f"Using DEFAULT voice")
            elif (voice in self.aliases):
                uds=UserDataService()
                uds.set_voice(ctx.author.id, ctx.channel.id, voice)
                await ctx.send(f"The new voice is '{voice}'")
        except:
            await ctx.send(f"Had trouble setting up the new voice.")
            await ctx.send(f"'{voice} is not valid voice.")
            
    async def _get_voice(self, user_id, channel_id):
        """
        Prints current users current voice profile.
        
        parameter:
            ctx [commands.Context]: discord Contxt object
        """
        try:
            uds = UserDataService()
            return uds.get_voice(user_id, channel_id)
        except:
            return self.default_voice
            
    @set_voice.error
    async def set_voice_error(self, ctx, error):
        """
        sends informational embed to be displayed if set voice command
        is being missused
        
        arguments:
            ctx:
            error:
        """
        if isinstance(error, commands.MissingRequiredArgument):
            voice = (await self._get_voice(ctx.author.id, ctx.channel.id))[0] #cache?
            prefix=ctx.prefix
            embed = Embed(title="Blabber Voice",
            description="Changes the voice used to send messages in "
            "Blabber bot. You can also use the bot by @mentioning it " 
            "instead of using the prefix. See list for all supported "
            "voices",
            colour=Colour.blue())
            
            embed.add_field(name="Current Voice:", value=f"`{voice}`")
            embed.add_field(name="Update Voice:", 
            value=f"`{prefix} voice [new voice or DEFAULT]`")
            await ctx.send(embed=embed)
            
def setup(bot):
    """
    Adds Settings Cog to bot.
    
    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Profiles(bot))
    