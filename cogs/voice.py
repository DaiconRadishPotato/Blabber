# voice.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 12/16/2019
# Date last modified: 3/29/2020
# Python Version: 3.8.1
# License: MIT License

from discord import ClientException
from discord.ext import commands

from blabber.checks import is_guild_owner, is_bot_alone
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
    @commands.check_any(is_guild_owner, commands.has_role("Blabby"), 
    is_bot_alone)
    async def disconnect_from_voice_channel(self, ctx):
        """
        Disconnects bot's voice client from it's current voice channel.
        Changes rich presence message to convey that the bot has left the voice
        channel.

        parameters:
            ctx [commands.Context]: discord Context object
        raises:
            CheckAnyFailure: Invoker does not have permission to use the bot ie
            not the guild owner, nor do they have "Blabby" role, and bot is not
            with other users.
            AttributeError: Bot is not connected to a voice channel
        """
        await ctx.send("Voice::disconnect_from_VC disconnecting from "
        f"{ctx.voice_client.channel}")
        await ctx.voice_client.disconnect()
        

    @commands.command(name='connect', aliases=['c'])
    @commands.check_any(is_guild_owner, commands.has_role("Blabby"),
    is_bot_alone)
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
            CheckAnyFailure: Invoker does not have permission to use the bot ie
            not the guild owner, nor do they have "Blabby" role, and bot is not
            with other users.
            AttributeError: Invoker is not in a voice channel.
            ClientException: Bot is already connected to a voice channel.
        """
        await ctx.author.voice.channel.connect()
        await ctx.send("Voice::connect_to_VC connecting to "
        f"{ctx.author.voice.channel.name}.")

    @commands.command(name='say', aliases=['s'])
    @commands.has_role("Blabby")
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

    @disconnect_from_voice_channel.error
    async def disconnect_error(self, ctx, error):
        # If user does not have permission to use 
        if isinstance(error, commands.CheckAnyFailure):
            await ctx.send("Voice::disconnect_from_voice_channel Bot is "
            "in use right now in a different channel. You require the blabby "
            "role or you need to try again later when it is not in use")
        # If bot is not connected, warn the invoker
        elif isinstance(error.original, AttributeError):
            await ctx.send("Voice::disconnect_from_VC Bot is not "
            "connected")

    @connect_to_voice_channel.error
    async def connect_error(self, ctx, error):
        if isinstance(error, commands.CheckAnyFailure):
            # If invoker is not in the have permission but the bot is
            # connected, warn the user that the bot is already connected
            if ctx.voice_client.channel == ctx.author.voice.channel:
                await ctx.send("Voice::connect_to_VC already connected to "
                f"{ctx.voice_client.channel.name}")
            else:
                # If invoker does not have permission to use bot, warn them
                await ctx.send("Voice::connect_to_VC Voice is in use right "
                "now in a different channel. You require the blabby role or "
                "you need to try again later when it is not in use")
        # If invoker is not in a voice channel, warm them
        elif isinstance(error.original, AttributeError):
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
        

def setup(bot):
    """
    Adds Voice Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Voice(bot))
