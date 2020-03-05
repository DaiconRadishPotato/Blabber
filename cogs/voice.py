# voice.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 12/16/2019
# Date last modified: 3/4/2020
# Python Version: 3.8.1
# License: "MIT"

from discord import Embed, Activity, ActivityType, ClientException, utils
from discord.ext import commands

@commands.check
async def is_guild_owner(ctx):
    """
    Checks if invoker is the owner of the guild.

    parameter:
        ctx [commands.Context]: discord Context object
    returns:
        boolean
    """
    return ctx.author == ctx.guild.owner

@commands.check
async def is_bot_alone(ctx):
    """
    Checks if bot is not in use.

    parameter:
        ctx [commands.Context]: discord Context object
    returns:
        boolean
    """
    # checks if voice is not even connected
    return ctx.voice_client == None or \
        len(ctx.voice_client.channel.members) == 1 or \
            (len(ctx.voice_client.channel.members) == 2 and \
                ctx.author.voice.channel == ctx.voice_client.channel)

class Voice(commands.Cog):
    """
    Voice Cog object that handles connection, disconnection, and voice client

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
        Changes rich presence message to show that bot is connected to the voice
        chat.
        If requester of connection is in a different voice channel, voice client
        will change.

        parameters:
            ctx [commands.Context]: discord Context object
        """
        # Check if voice client is alone and is requested to another channel
        await ctx.author.voice.channel.connect()
        await ctx.send("Voice::connect_to_VC connecting to "
        f"{ctx.author.voice.channel.name}.")

    @commands.command(name='say', aliases=['s'])
    @commands.has_role("Blabby")
    async def say_message(self, ctx, *message: str):
        """
        To be created

        parameters:
            ctx [commands.Context]: discord Context object
            *message [str]: array of words to be joined
        """
        if ctx.voice_client is None:
            await self.connect_to_voice_channel(ctx)
            
        if ctx.voice_client is not None and len(message) != 0:
            message = ' '.join(message)
            if len(message) > 600:
                await ctx.send("Voice::say_message Please make your message "
                               "shorter. We have set the character limit to"
                               "600 to be considerate for others.")
                return
            print(message)
        else:
            await ctx.send("Voice::say_message Please input a message")

    @disconnect_from_voice_channel.error
    async def disconnect_error(self, ctx, error):
        # If bot is not connected to any voice channel in the guild
        if isinstance(error, commands.CheckAnyFailure):
            await ctx.send("Voice::disconnect_from_voice_channel Bot is "
            "in use right now in a different channel. You require the blabby "
            "role or you need to try again later when it is not in use")
        elif isinstance(error.original, AttributeError):
            await ctx.send("Voice::disconnect_from_VC Bot is not "
            "connected")

    @connect_to_voice_channel.error
    async def connect_error(self, ctx, error):
        # If author is not in a voice channel to join
        if isinstance(error, commands.CheckAnyFailure):
            if ctx.voice_client.channel == ctx.author.voice.channel:
                await ctx.send("Voice::connect_to_VC already connected to "
                f"{ctx.voice_client.channel.name}")
            else:
                await ctx.send("Voice::connect_to_VC Voice is in use right "
                "now in a different channel. You require the blabby role or you"
                " need to try again later when it is not in use")
        elif isinstance(error.original, AttributeError):
            await ctx.send("Voice::connect_to_VC You need to be connected to "
            "a voice channel to use this command.")
        # If bot is already connected to the same voice channel as author
        elif isinstance(error.original, ClientException):
            if ctx.voice_client.channel == ctx.author.voice.channel:
                await ctx.send("Voice::connect_to_VC already connected to "
                f"{ctx.voice_client.channel.name}")
            else:
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
