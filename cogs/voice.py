# voice.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 12/16/2019
# Date last modified: 3/9/2020
# Python Version: 3.8.1
# License: MIT License

import functools

from discord import Embed, Activity, ActivityType, ClientException, utils
from discord.ext import commands

from blabber.checks import can_disconnect_bot
from blabber.errors import *
from blabber.request import TTSRequest, TTSRequestHandler
from blabber.player import TTSAudio


class Voice(commands.Cog):
    """
    Collection of commands for handling connection to Discord voice channel.

    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='disconnect', aliases=['dc'])
    @can_disconnect_bot()
    async def disconnect(self, ctx):
        """
        Disconnects Blabber from the voice channel it's currently in.

        parameters:
            ctx [commands.Context]: discord Context object
        raises:
            AttributeError: when Blabber is not connected to a voice channel
        """
        await ctx.voice_client.disconnect()
        await ctx.send(":white_check_mark: **Successfully disconnected**")
            
        
    @disconnect.error
    async def disconnect_error(self, ctx, error):
        """
        Local error handler for Blabber's disconnect command.

        parameters:
            ctx [commands.Context]: discord Context object
            error [Exception]: error object thrown by command
        """
        # Check if error was caused by an uninitialized voice client
        await ctx.send(":x: **Unable to disconnect**\n" + str(error))

    @commands.command(name='connect', aliases=['c'])
    async def connect(self, ctx):
        """
        Creates a voice client with voice channel for discord bot to speak
        through.
        If requester of connection is in a different voice channel, voice 
        client will change.

        parameters:
            ctx [commands.Context]: discord Context object
        raises:
            AttributeError: Invoker is not in a voice channel.
            ClientException: Bot is already connected to a voice channel.
        """
        if ctx.voice_client:
            if can_disconnect(ctx):
                await ctx.voice_client.move_to(ctx.author.voice.channel)
                await ctx.send(f":white_check_mark: **Moved to** `{ctx.author.voice.channel.name}`")
            else:
                await ctx.send(":x: **Unable to move**\n`Blabby` role or `Manage Channels` permission required when others are in voice channel")
        else:
            await ctx.author.voice.channel.connect()
            await ctx.send(f":white_check_mark: **Connected to** `{ctx.author.voice.channel.name}`")

        print(ctx.author.voice.channel)
        #for member in ctx.voice_client.channel.members:
        #    print(member)
        #    for perm in member.permissions_in(ctx.author.voice.channel):
        #        print(perm)
    
    @connect.error
    async def connect_error(self, ctx, error):
        """
        Local error handler for Blabber's connect command.

        parameters:
            ctx [commands.Context]: discord Context object
            error [Exception]: error object thrown by command function
        """
        print(error)
        # Check if error was caused by a context author that wasn't in a voice channel
        if isinstance(error.original, AttributeError):
            await ctx.send(":x: **Unable to connect**\nActive voice channel required for Blabber to connect")

    @commands.command(name='say', aliases=['s'])
    async def say(self, ctx, *, message):
        """
        To be created

        parameters:
            ctx [commands.Context]: discord Context object
            *message [str]: array of words to be joined
        """
        if ctx.voice_client is None:
            await self.connect_to_voice_channel(ctx)
            
        if ctx.voice_client is not None and len(message) != 0:
            if len(message) <= 600:
                request = TTSRequest(message)
                handle = TTSRequestHandler(request)
                source = TTSAudio(handle)
                ctx.voice_client.play(source)
            else:
                await ctx.send("Voice::say_message Please make your message "
                               "shorter. We have set the character limit to"
                               "600 to be considerate for others.")
        else:
            await ctx.send("Voice::say_message Please input a message")
    
    @say.error
    async def say_error(self, ctx, error):
        None

def setup(bot):
    """
    Adds Voice Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Voice(bot))
