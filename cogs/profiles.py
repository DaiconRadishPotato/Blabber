# profiles.py
#
# Author: Fanny Avila (Fa-Avila)
# Contributor:  Jacky Zhang (jackyeightzhang),
#               Marcos Avila (DaiconV)
# Date created: 3/27/2020
# Date last modified: 4/17/2020
# Python Version: 3.8.1
# License: MIT License

import json
from discord.ext import commands
from discord import Embed, Colour
from blabber.user_services import UserDataService
from blabber.guild_services import GuildDataService


class Profiles(commands.Cog):
    """
    Profiles Cog Object that is a collection of commands for managing 
    user's voice profiles
    
    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.DEFAULT_VOICE = (
            'voice_1', 
            'de-DE-Standard-F', 
            'FEMALE', 
            'de', 
            'de-DE'
        )
        self.bot = bot
        self.aliases = set()
        
        #reading in voice aliases from json into set
        with open(r'./blabber/voices.json', 'r') as f:
            voice_dict=json.load(f)
            
            for voice in voice_dict['voices']:
                self.aliases.add(voice['alias'])
                
    @commands.command(name='voice', aliases=['v'])
    async def set_voice(self, ctx, *, alias):
        """
        Sets up and updates a user voice profile.
        
        parameter:
            ctx [commands.Context]: discord Contxt object
            alias [str]: string representing a specific alias
        """
        alias=alias.lower()
        
        if alias == self.DEFAULT_VOICE[0]:
            try:
                uds=UserDataService()
                uds.remove_voice(ctx.author.id, ctx.channel.id)
                await ctx.send(f":white_check_mark: "
                    f"**The new voice is** '{alias}'")
            except:
                await ctx.send(f":x: "
                    f"**Had trouble setting up the new voice.**")
                await ctx.send(f"Try again at a later time")
                
        elif (alias in self.aliases):
            try:
                uds=UserDataService()
                uds.set_voice(ctx.author.id, ctx.channel.id, alias)
                await ctx.send(f":white_check_mark: "
                    f"**The new voice is **'{alias}'")
            except:
                await ctx.send(f":x: "
                    f"**Had trouble setting up the new voice.**")
                await ctx.send(f"Try again at a later time")
                
        else:
            await ctx.send(f":x: **`{alias}` is not a valid voice**")
            
    async def _get_voice(self, user_id, channel_id):
        """
        Prints current users current voice profile.
        
        parameter:
            ctx [commands.Context]: discord Contxt object
        returns:
            voice [tuple]: of voice information from database
        """
        try:
            uds = UserDataService()
            voice = uds.get_voice(user_id, channel_id)
            if voice is None:
                voice = self.DEFAULT_VOICE
            return voice
        except:
            pass
            
    @set_voice.error
    async def set_voice_error(self, ctx, error):
        """
        Sends informational embed to be displayed if set voice command
        is being missing arguments
        """
        if isinstance(error, commands.MissingRequiredArgument):
            voice = (await self._get_voice(ctx.author.id, ctx.channel.id))[0] #cache?
            prefix= (await self.bot.get_cog("Settings")._get_prefix(ctx.guild.id))
            member=ctx.message.author
            embed = Embed(title="Blabber Voice",
            description="Changes the voice used to send messages in "
            "Blabber bot. You can also use the bot by @mentioning it " 
            "instead of using the prefix. See list for all supported "
            "voices",
            colour=Colour.blue())
            
            embed.add_field(name=f"{member}'s current Voice:", 
            value=f"`{voice}`")
            embed.add_field(name="Update Voice:", 
            value=f"`{prefix}v [new voice]`")
            await ctx.send(embed=embed)
            
def setup(bot):
    """
    Adds Settings Cog to bot.
    
    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Profiles(bot))
    