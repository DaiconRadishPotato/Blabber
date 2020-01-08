# blabber.py
# Author: Fanny Avila (Fa-Avila), Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 12/16/2019
# Date last modified: 1/7/2020
# Python Version: 3.7.4
# License: "MIT"

from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
from multiprocessing import Process, Queue
from time import perf_counter
from asyncio import sleep
from google.cloud import texttospeech
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
DISCORD_TOKEN = getenv('discord_token')
GOOGLE_APPLICATION_CREDENTIALS = getenv('google_application_credentials')

bot = commands.Bot(command_prefix='>')


class BlabberBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._queue = Queue()

    @commands.command(
        name='disconnect',
        aliases=['dc'],
        help='Disconnect Blabber from the server it is in')
    async def disconnect_from_voice_channel(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("Blabber::disconnect_from_VC "
                           "Blabber is not connected")
        elif ctx.voice_client.is_playing():
            await ctx.send("Blabber::disconnect_from_VC "
                           "Blabber is still talking")
        elif (len(ctx.voice_client.channel.members) == 1 or
              ctx.author in ctx.voice_client.channel.members):
            await ctx.send("Blabber::disconnect_from_VC "
                           f"disconnecting from {ctx.voice_client.channel}")
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("Blabber::disconnect_from_VC "
                           "You need to be in a voice "
                           "channel to use this command.")

    @commands.command(
        name='connect',
        aliases=['c'],
        help='Connect Blabber to the same server you are in')
    async def connect_to_voice_channel(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Blabber::connect_to_VC "
                           "You need to be in a voice "
                           "channel to use this command.")
        elif ctx.voice_client is None:
            await ctx.send("Blabber::connect_to_VC "
                           f"connecting to {ctx.author.voice.channel.name}.")
            await ctx.author.voice.channel.connect()
        elif ctx.voice_client.channel == ctx.author.voice.channel:
            await ctx.send("Blabber::connect_to_VC "
                           f"already connected to "
                           "{ctx.voice_client.channel.name}")
        elif len(ctx.voice_client.channel.members) == 1:
            await ctx.send("Blabber::connect_to_VC "
                           f"swaping from {ctx.voice_client.channel.name} "
                           f"to {ctx.author.voice.channel.name}")
            await ctx.voice_client.move_to(ctx.author.voice.channel)
        else:
            await ctx.send("Blabber::connect_to_VC Not sure what happened")

    @commands.command(name='say', aliases=['s'])
    async def say_message(self, ctx, *message: str):
        message = ' '.join(message)
        self._queue.put(message)
        print(message)
        audio = await self.create_voice(ctx)
        await self.send_voice(ctx, audio)


def setup(bot):
    bot.add_cog(BlabberBot(bot))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Blabber::on_command_error '
                       f'"{ctx.message.content}" '
                       'is not a command for Blabber.')
    else:
        await ctx.send(error)

if __name__ == "__main__":
    try:
        setup(bot)
    except Exception as exception:
        print("Tried loading cog but didnt work")
        print(exception)
    finally:
        bot.run(DISCORD_TOKEN)
