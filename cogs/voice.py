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

from blabber.checks import has_role, has_permission
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
    async def disconnect_from_voice_channel(self, ctx):
        """
        Disconnects Blabber from the voice channel it's currently in.

        parameters:
            ctx [commands.Context]: discord Context object
        raises:
            AttributeError: when Blabber is not connected to a voice channel
        """
        # Count number of users in voice channel excluding context author and bots
        user_count = 0
        for member in ctx.voice_client.channel.members:
            user_count += (not member.bot and member.id != ctx.author.id)

        # Check whether context is valid to execute this command
        if has_role(ctx, 'Blabby') or has_permission(ctx, 'manage_channels') or user_count == 0:
            await ctx.send(":white_check_mark: **Successfully disconnected**")
            await ctx.voice_client.disconnect()
        else:
            await ctx.send(":x: **Unable to disconnect**\n`Blabby` role or `Manage Channels` permission required when others are in voice channel")
            
        
    @disconnect_from_voice_channel.error
    async def disconnect_error(self, ctx, error):
        """
        Local error handler for Blabber's disconnect command.

        parameters:
            ctx [commands.Context]: discord Context object
            error [Exception]: error object thrown by command
        """
        # Check error 
        if isinstance(error.original, AttributeError):
            await ctx.send(":x: **Unable to disconnect**\nBlabber is currently not connected to any voice channel")


    @commands.command(name='connect', aliases=['c'])
    async def connect_to_voice_channel(self, ctx):
        """
        Creates a voice client with voice channel for discord bot to speak
        through.
        Changes rich presence message to show that bot is connected to the 
        voice chat.
        If requester of connection is in a different voice channel, voice 
        client will change.

        parameters:
            ctx [commands.Context]: discord Context object
        raises:
            AttributeError: Invoker is not in a voice channel.
            ClientException: Bot is already connected to a voice channel.
        """
        await ctx.author.voice.channel.connect()
        await ctx.send(f":white_check_mark: **Joined** `{ctx.author.voice.channel.name}`")

    @connect_to_voice_channel.error
    async def connect_error(self, ctx, error):
        # If invoker is not in a voice channel, warm them
        if isinstance(error.original, AttributeError):
            await ctx.send("Voice::connect_to_VC You need to be connected to "
            "a voice channel to use this command.")
        elif isinstance(error.original, ClientException):
            # If bot is already connected to the same voice channel as author
            if ctx.voice_client.channel == ctx.author.voice.channel:
                await ctx.send("Voice::connect_to_VC already connected to "
                f"{ctx.voice_client.channel.name}")
            else:
                # If bot is in a different voice channel than the invoker, 
                # switch channels 
                await ctx.send("Voice::connect_to_VC swaping from "
                f"{ctx.voice_client.channel.name} to "
                f"{ctx.author.voice.channel.name}")
                await ctx.voice_client.move_to(ctx.author.voice.channel)

    @commands.command(name='say', aliases=['s'])
    async def say_message(self, ctx, *, message:str):
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


        

def setup(bot):
    """
    Adds Voice Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Voice(bot))
