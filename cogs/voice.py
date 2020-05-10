# voice.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 12/16/2019
# Date last modified: 5/4/2020
# Python Version: 3.8.1
# License: MIT License

from discord import ClientException
from discord.ext import commands


from blabber.checks import *

from blabber.audio import TTSAudio
from blabber.request import TTSRequest
from blabber.pool import TTSRequestHandlerPool

class Voice(commands.Cog):
    """
    Collection of commands for handling connection to Discord voice channel.

    parameters:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot

        self._pool = TTSRequestHandlerPool()

    def cog_unload(self):
        self._pool.teardown()

    async def _summon_blabber(self, ctx):
        if ctx.voice_client:
            await can_disconnect(ctx)
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            return 'Moved'
        else:
            await ctx.author.voice.channel.connect()
            return 'Connected'

    @commands.command(name='connect', aliases=['c'])
    @commands.check(is_connected)
    @commands.check(blabber_has_required_permissions)
    async def connect(self, ctx):
        """
        Connects Blabber to the voice channel the command invoker is connected to.

        parameters:
            ctx [commands.Context]: discord Context object
        raises:
        """
        if ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.send(":information_source: **Blabber is already in this voice channel**")
        else:     
            operation = await self._summon_blabber(ctx)
            await ctx.send(f":white_check_mark: **{operation} to** `{ctx.author.voice.channel.name}`")
        
    @commands.command(name='disconnect', aliases=['dc'])
    async def disconnect(self, ctx):
        """
        Disconnects Blabber from the voice channel it is connected to.

        parameters:
            ctx [commands.Context]: discord Context object
        raises:
            
        """
        if not ctx.voice_client:
            await ctx.send(":information_source: **Blabber is not in any voice channel**")
        else:
            await can_disconnect(ctx)
            await ctx.voice_client.disconnect()
            await ctx.send(":white_check_mark: **Successfully disconnected**")


    @commands.command(name='say', aliases=['s'])
    @commands.check(is_connected)
    @commands.check(tts_message_is_valid)
    async def say(self, ctx, *, message:str):
        """
        To be created

        parameters:
            ctx [commands.Context]: discord Context object
            *message [str]: array of words to be joined
        """
        if not ctx.voice_client or ctx.author.voice.channel != ctx.voice_client.channel:
            await blabber_has_required_permissions(ctx)
            await self._summon_blabber(ctx)
            
        request = TTSRequest(message)
        if ctx.voice_client._player:
            audio = ctx.voice_client._player.source
        else:
            audio = TTSAudio(self._pool)

        await audio.submit_request(request)

        if not ctx.voice_client.is_playing():
            ctx.voice_client.play(audio)

        await ctx.message.add_reaction('📣')

    @disconnect.error
    async def disconnect_error(self, ctx, error):
        """
        Local error handler for Blabber's disconnect command.

        parameters:
            ctx [commands.Context]: discord Context object
            error [Exception]: error object thrown by command
        """
        await ctx.send(f":x: **Unable to disconnect**\n{error}")

    @connect.error
    async def connect_error(self, ctx, error):
        """
        Local error handler for Blabber's connect command.

        parameters:
            ctx [commands.Context]: discord Context object
            error [Exception]: error object thrown by command function
        """
        # Check what kind of operation caused error
        operation = 'move' if ctx.voice_client else 'connect'
        await ctx.send(f":x: **Unable to {operation}**\n{error}")
    
    @say.error
    async def say_error(self, ctx, error):
        if not isinstance(error, TTSMessageTooLong):
            operation = 'move' if ctx.voice_client else 'connect'
            await ctx.send(f":x: **Unable to {operation}**\n{error}")
        else:
            await ctx.send(f":x: **Unable to convert to speech**\n{error}")
                
def setup(bot):
    """
    Adds Voice Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Voice(bot))
