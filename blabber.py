# blabber.py
#
# Author: Jacky Zhang (jackyeightzhang)
# Contributor:  Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV)
# Date created: 12/16/2019
# Date last modified: 5/28/2020
# Python Version: 3.8.1
# License: MIT License

import asyncio
import json
import logging
import os

from discord.ext import commands
from dotenv import load_dotenv

from blabber.cache import VoiceProfileCache, PrefixCache
from blabber.pool import TTSRequestHandlerPool

load_dotenv()


def _prefix_callable(bot, message):
    """
    Determines whether a user message is a command by checking if it has a
    specified prefix or @mention

    parameters:
        bot [Bot]: client object representing a Discord bot
        message [Message]: the message or context from the guild that 
                               called the bot.
    returns:
        callable:
    """
    return commands.when_mentioned_or(bot.prefixes[message.guild])(bot, message)


def load_cog_files(bot):
    """
    Traverse through cogs directory and loads each cog module in the directory.
    
    parameter:
        bot [Bot]: client object representing a Discord bot
    """
    for cog in os.listdir("cogs"):
        if cog.endswith(".py"):
            try:
                cogs = f"cogs.{cog.replace('.py','')}"
                bot.load_extension(cogs)
                print(f"{cog} loaded in")
            except Exception as exception:
                print(f"{cog} can not be loaded:\n{exception}")
                
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

    pool = TTSRequestHandlerPool()
    try:
        bot = commands.Bot(command_prefix=_prefix_callable, help_command=None)

        bot.pool = pool
        bot.voice_profiles = VoiceProfileCache()
        bot.prefixes = PrefixCache()

        load_cog_files(bot)
        bot.run(os.getenv('discord_token'))
    finally:
        pool.teardown()
