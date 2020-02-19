# blabber.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 12/16/2019
# Date last modified: 2/18/2020
# Python Version: 3.8.1
# License: "MIT"

from discord import Embed, Activity, ActivityType
from discord.ext import commands

class Blabber(commands.Cog):
    """
    Blabber Cog object that handles connection, disconnection, and voice client

    attributes:
        bot [discord.Bot]: discord Bot object
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='disconnect', aliases=['dc'])
    @commands.has_role("Blabby")
    async def disconnect_from_voice_channel(self, ctx):
        """
        Disconnects bot's voice client from it's current voice channel.
        Changes rich presence message to convey that the bot has left the voice
        channel.

        parameters:
            ctx [commands.Context]: discord Context object
        """
        await self.bot.change_presence(
            activity=Activity(name="outside the Voice Chat",
            type=ActivityType.playing))
        # Checks if bot is not connected to any voice channel in the guild
        if ctx.voice_client is None:
            await ctx.send("Blabber::disconnect_from_VC Blabber is not "
            "connected")
        # Checks if voice client is the only one in the voice channel or author
        # is in voice channel
        elif (len(ctx.voice_client.channel.members) == 1 or
              ctx.author in ctx.voice_client.channel.members):
            await ctx.send("Blabber::disconnect_from_VC disconnecting from "
                           f"{ctx.voice_client.channel}")
            await ctx.voice_client.disconnect()
        else:
            # Checks if author is not in voice channel
            await ctx.send("Blabber::disconnect_from_VC You need to be in a "
            "voice channel to use this command.")

    @commands.command(name='connect', aliases=['c'])
    @commands.has_role("Blabby")
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
        await self.bot.change_presence(
            activity=Activity(name="in the Voice Chat",
            type=ActivityType.playing))
        # Checks if invoker is in a voice channel to join
        if ctx.author.voice is None:
            await ctx.send("Blabber::connect_to_VC You need to be in a voice "
                           "channel to use this command.")
        # Checks if bot is not already connected to a voice channel
        elif ctx.voice_client is None:
            await ctx.send("Blabber::connect_to_VC connecting to "
            "{ctx.author.voice.channel.name}.")
            await ctx.author.voice.channel.connect()
        # Checks if bot is already connected to the same voice channel as 
        # invoker
        elif ctx.voice_client.channel == ctx.author.voice.channel:
            await ctx.send("Blabber::connect_to_VC already connected to "
                           f"{ctx.voice_client.channel.name}")
        # Check if voice client is alone and is requested to another channel
        elif len(ctx.voice_client.channel.members) == 1:
            await ctx.send("Blabber::connect_to_VC "
                           f"swaping from {ctx.voice_client.channel.name} "
                           f"to {ctx.author.voice.channel.name}")
            await ctx.voice_client.move_to(ctx.author.voice.channel)
        else:
            # When voice client is in another channel with other users
            await ctx.send("Blabber::connect_to_VC Blabber is in use right now "
            "in a different channel please try again later")
        
    @commands.command(name='say', aliases=['s'])
    @commands.has_role("Blabby")
    async def say_message(self, ctx, *message: str):
        """
        To be created

        parameters:
            ctx [commands.Context]: discord Context object
            *message [str]: array of words to be joined
        """
        await self.bot.change_presence(
            activity=Activity(name="what people have to say",
            type=ActivityType.listening))
        if ctx.voice_client is None:
            await self.connect_to_voice_channel(ctx)
            
        if ctx.voice_client is not None and len(message) != 0:
            message = ' '.join(message)
            if len(message) > 600:
                await ctx.send("Blabber::say_message Please make your message "
                               "shorter. We have set the character limit to"
                               "600 to be considerate for others.")
                return
            print(message)
        else:
            await ctx.send("Blabber::say_message Please input a message")


def setup(bot):
    """
    Adds Blabber Cog to bot.

    parameter: 
        bot [discord.Bot]: discord Bot object
    """
    bot.add_cog(Blabber(bot))
