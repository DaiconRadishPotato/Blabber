# voice.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 12/16/2019
# Date last modified: 6/2/2020
# Python Version: 3.8.1
# License: MIT License

from discord import Embed, Colour
from discord.ext import commands

from blabber import supported_voices
from blabber.audio import TTSAudio
from blabber.checks import *
from blabber.errors import *
from blabber.request import TTSRequest


class Voice(commands.Cog):
    """
    Collection of commands for handling connection to Discord voice channel.

    parameters:
        bot [Bot]: client object representing a Discord bot
    """
    def __init__(self, bot):
        self.pool = bot.pool
        self.voice_profiles = bot.voice_profiles

    async def _connect(self, ctx):
        """
        Helper method for connecting Blabber to the command invoker's voice
        channel.

        parameters:
            ctx [Context]: context object representing command invocation
        returns:
            str: voice channel operation performed by Blabber
        """
        # Check if Blabber is currently connected to a voice channel
        if ctx.voice_client:
            await can_disconnect(ctx)
            await blabber_has_required_permissions(ctx)

            # Clear audio channel before moving Blabber
            player = ctx.voice_client._player
            if player is not None:
                player.source.clear()

            # Move Blabber to the command invoker's voice channel
            await ctx.voice_client.move_to(ctx.author.voice.channel)
            return 'Moved'
        else:
            await blabber_has_required_permissions(ctx)

            # Connect Blabber to the command invoker's voice channel
            await ctx.author.voice.channel.connect()
            return 'Connected'

    @commands.command(name='connect', aliases=['c'])
    @commands.check(is_connected)
    async def connect(self, ctx):
        """
        Connects Blabber to the voice channel the command invoker is connected
        to.

        parameters:
            ctx [Context]: context object representing command invocation
        """
        # Check if Blabber is connected to command invoker's voice channel
        if (ctx.voice_client
            and ctx.author.voice.channel == ctx.voice_client.channel):
            embed = Embed(
                title=(":information_source: **Blabber is already in this "
                       "voice channel**"),
                colour=Colour.blue())
        else:
            operation = await self._connect(ctx)
            embed = Embed(
                title=(f":white_check_mark: **{operation} to** "
                       f"`{ctx.author.voice.channel.name}`"),
                colour=Colour.green())

        await ctx.send(embed=embed)

    @commands.command(name='disconnect', aliases=['dc'])
    async def disconnect(self, ctx):
        """
        Disconnects Blabber from the voice channel it is connected to.

        parameters:
            ctx [Context]: context object representing command invocation
        """
        # Check if Blabber is currently connected to a voice channel
        if not ctx.voice_client:
            embed = Embed(
                title=(":information_source: **Blabber is not connected to "
                       "any voice channel**"),
                colour=Colour.blue())
        else:
            await can_disconnect(ctx)

            # Disconnect Blabber from voice channel
            await ctx.voice_client.disconnect()
            embed = Embed(
                title=":white_check_mark: **Successfully disconnected**",
                colour=Colour.green())

        await ctx.send(embed=embed)

    @commands.command(name='say', aliases=['s'])
    @commands.check(is_connected)
    async def say(self, ctx, *, message: str=''):
        """
        Recites a message into the voice channel the command invoker is
        connected to.

        parameters:
            ctx [Context]: context object representing command invocation
            message [str]: message to recite
        """
        # Ensure message is not empty
        if not message:
            embed = Embed(
                title=":information_source: **No message to recite**",
                colour=Colour.blue())
            await ctx.send(embed=embed)
        elif await tts_message_is_valid(message):
            # Ensure Blabber is connected to command invoker's voice channel
            if (not ctx.voice_client
                or ctx.author.voice.channel != ctx.voice_client.channel):
                await self._connect(ctx)

            # Check if AudioSource object already exists
            if ctx.voice_client._player:
                audio = ctx.voice_client._player.source
            else:
                audio = TTSAudio(self.pool)

            # Retrieve command invoker's voice profile
            alias = self.voice_profiles[(ctx.author, ctx.channel)]
            voice = supported_voices[alias]

            # Submit TTS request
            request = TTSRequest(message, **voice)
            await audio.submit_request(request)

            # Ensure AudioSource object is playing
            if not ctx.voice_client.is_playing():
                ctx.voice_client.play(audio)

            await ctx.message.add_reaction('📣')

    @connect.error
    async def connect_error(self, ctx, error):
        """
        Local error handler for Blabber's connect command.

        parameters:
            ctx     [Context]: context object representing command invocation
            error [Exception]: exception object raised from command function
        """
        # Check what type of voice channel operation caused the error
        operation = 'move' if ctx.voice_client else 'connect'

        embed = Embed(
            title=f":x: **Unable to {operation}**",
            colour=Colour.red())

        if (isinstance(error, BlabberConnectError) 
            or isinstance(error, NotConnected)):
            embed.description=f"{error}"

        else:
            embed.description=("**Unexpected Error**\n"
                               "Please contact development team")

        await ctx.send(embed=embed)

    @disconnect.error
    async def disconnect_error(self, ctx, error):
        """
        Local error handler for Blabber's disconnect command.

        parameters:
            ctx     [Context]: context object representing command invocation
            error [Exception]: exception object raised from command function
        """
        embed = Embed(title=f":x: **Unable to disconnect**",colour=Colour.red())

        if isinstance(error, MissingCredentials):
            embed.description=f"{error}"

        else:
            embed.description=("**Unexpected Error**\n"
                               "Please contact development team")

        await ctx.send(embed=embed)

    @say.error
    async def say_error(self, ctx, error):
        """
        Local error handler for Blabber's say command.

        parameters:
            ctx     [Context]: context object representing command invocation
            error [Exception]: exception object raised from command function
        """
        if isinstance(error, BlabberConnectError):
            await self.connect_error(ctx, error)
            return None

        elif (isinstance(error, TTSMessageTooLong)
              or isinstance(error, NotConnected)):
            embed = Embed(
                title=f":x: **Unable to convert to speech**",
                description=f"{error}",
                colour=Colour.red())

        else:
            embed = Embed(
                title=f":x: **Unable to convert to speech**",
                description=("**Unexpected Error**\n"
                             "Please contact development team"),
                colour=Colour.red())

        await ctx.send(embed=embed)


def setup(bot):
    """
    Adds Voice Cog to bot.

    parameter:
        bot [Bot]: client object representing a Discord bot
    """
    bot.add_cog(Voice(bot))
