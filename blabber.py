# blabber.py
# Author: Fanny Avila (Fa-Avila),
# Marcos Avila (DaiconV),
# and Jacky Zhang (jackyeightzhang)
# Date created: 12/16/2019
# Date last modified: 3/4/2020
# Python Version: 3.8.1
# License: "MIT"

import os
import logging
import json
import asyncio

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('discord_token')


def get_prefix(bot, message): # add async when retrieving from database
    """
    Checks a json file to see if guild has a different prefix and return it.
    Return the original prefix if guild is not in json file.

    parameters:
        bot [discord.Bot]: discord Bot object
        message [discord.Message]: the message or context from the guild that 
        called the bot.
    raises:
        IOError: raised when file does not exist
    returns:
        prefix: string that is used to call commands from the bot client
    """
    try:
        with open("prefixes.json", "r") as file:
            prefixes = json.load(file)
        # Checks if guild from the context exists within json file.
        if str(message.guild.id) not in prefixes:
            return commands.when_mentioned_or(">")(bot, message)
    except:
        return commands.when_mentioned_or(">")(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot, message)

def load_cog_files(bot):
    """
    Traverse through cogs directory and loads each cog module in the directory.

    parameter:
        bot [discord.Bot]: discord Bot object
    raises:
        ExtensionNotFound: The extension could not be imported.
        ExtensionAlreadyLoaded: The extension is already loaded.
        NoEntryPointErro: The extension does not have a setup function.
        ExtensionFailed: The extension or its setup function had an execution 
        error.
    """
    for cog in os.listdir("cogs"):
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

    load_cog_files(bot)
    bot.run(DISCORD_TOKEN)
