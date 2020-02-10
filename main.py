# main.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 12/16/2019
# Date last modified: 2/4/2020
# Python Version: 3.8.1
# License: "MIT"

from os import getenv, listdir
import logging
from discord import Activity, ActivityType
from discord.ext import commands
from dotenv import load_dotenv
from json import load
from asyncio import sleep

load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = getenv('google_application_credentials')
DISCORD_TOKEN = getenv('discord_token')


def get_prefix(bot, message): # add async when retrieving from database
    if not message.guild:
        return commands.when_mentioned_or(">")(bot, message)

    with open("prefixes.json", "r") as file:
        prefixes = load(file)
    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or(">")(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot, message)

async def change_presence(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=Activity(
            name=">help | Join a voice channel and use "
            ">say [message] to make me say something",
            type=ActivityType.listening))
        await sleep(15)

def load_cog_files(bot):
    for cog in listdir(".\\cogs"):
        if cog.endswith(".py"):
            try:
                cogs = f"cogs.{cog.replace('.py','')}"
                bot.load_extension(cogs)
                print(f"{cog} loaded in")
            except Exception as exception:
                print(f"{cog} can not be loaded: ")
                raise exception

if __name__ == "__main__":
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(
        filename='discord.log',
        encoding='utf-8',
        mode='w')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    bot = commands.Bot(command_prefix=get_prefix)

    @bot.event
    async def on_ready():
        print(f"{bot.user.name} logged in")
        print("------------------")
    
    load_cog_files(bot)
    bot.loop.create_task(change_presence(bot))
    bot.run(DISCORD_TOKEN)
