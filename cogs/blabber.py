# blabber.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 12/16/2019
# Date last modified: 2/6/2020
# Python Version: 3.8.1
# License: "MIT"

from discord import Embed, Activity, ActivityType
from discord.ext import commands
from multiprocessing import Process, Queue
from google.cloud import texttospeech
       
class Blabber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._message_queue = Queue()
        self._audio_queue = Queue()

    
    @commands.command(name='disconnect', aliases=['dc'])
    @commands.has_role("Blabby")
    async def disconnect_from_voice_channel(self, ctx):
        await self.bot.change_presence(activity=Activity(name="outside the Voice Chat",
                                                         type=ActivityType.playing))
        if ctx.voice_client is None:
            await ctx.send("Blabber::disconnect_from_VC "
                           "Blabber is not connected")
        elif ctx.voice_client.is_playing():
            await ctx.send("Blabber::disconnect_from_VC "
                           "Blabber is still talking")
        elif (len(ctx.voice_client.channel.members) == 1 or     # When the voice client is the
              ctx.author in ctx.voice_client.channel.members):  # only one connected or when
            await ctx.send("Blabber::disconnect_from_VC "       # author is in voice channel
                           "disconnecting from "
                           f"{ctx.voice_client.channel}")
            await ctx.voice_client.disconnect()
        else:                                                   # When author is not in voice
            await ctx.send("Blabber::disconnect_from_VC "       # channel
                           "You need to be in a voice "
                           "channel to use this command.")

    @commands.command(name='connect', aliases=['c'])
    @commands.has_role("Blabby")
    async def connect_to_voice_channel(self, ctx):
        await self.bot.change_presence(activity=Activity(name="in the Voice Chat",
                                                         type=ActivityType.playing))                
        if ctx.author.voice is None:
            await ctx.send("Blabber::connect_to_VC "
                           "You need to be in a voice "
                           "channel to use this command.")
        elif ctx.voice_client is None:
            await ctx.send("Blabber::connect_to_VC "
                           f"connecting to {ctx.author.voice.channel.name}.")
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel == ctx.author.voice.channel:  # When author and voice client
            await ctx.send("Blabber::connect_to_VC "                # are in the same channel
                           "already connected to "
                           f"{ctx.voice_client.channel.name}")
        elif len(ctx.voice_client.channel.members) == 1:            # When voice client is alone and
            await ctx.send("Blabber::connect_to_VC "                # is requested to another channel
                           f"swaping from {ctx.voice_client.channel.name} "
                           f"to {ctx.author.voice.channel.name}")
            await ctx.voice_client.move_to(ctx.author.voice.channel)
        else:                                                       # When voice client is in another
            await ctx.send("Blabber::connect_to_VC Blabber is in a "# channel with other users
                           "different channel right now")
        
    @commands.command(name='say', aliases=['s'])
    @commands.has_role("Blabby")
    async def say_message(self, ctx, *message: str):
        await self.bot.change_presence(activity=Activity(name="what people have to say",
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
            self._message_queue.put(message)
            print(message)
##        audio = await self.create_voice(ctx)
##        await self.send_voice(ctx, audio)
        else:
            await ctx.send("Blabber::say_message Please input a message")        

    @commands.command(name='list', aliases=['l'])
    @commands.has_role("Blabby")
    async def display_voice_profile(self, ctx, *flags: str):
        await ctx.send("Blabber::display_voice_profile")

    @commands.command(name='voice', aliases=['v'])
    @commands.has_role("Blabby")
    async def make_voice_profile(self, ctx):
        await ctx.send("Blabber::make_voice_profile")


def setup(bot):
    bot.add_cog(Blabber(bot))
