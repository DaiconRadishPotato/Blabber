# errors.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Jacky Zhang (jackyeightzhang)
# Date created: 4/3/2020
# Date last modified: 4/4/2020
# Python Version: 3.8.1
# License: MIT License

from discord.ext import commands

class BotNotConnected(commands.CommandError):
    def __init__(self):
        super().__init__("Blabber is currently not connected to any voice channel")

class BotMissingVoiceChannelPermissions(commands.CommandError):
    def __init__(self, channel_name):
        super().__init__(f"Blabber does not have permission to connect to `{channel_name}`")

class BotConnectedToAnotherChannel(commands.CommandError):
    def __init__(self):
        super().__init__("Blabber is connected to another voice channel")

class MessageTooLong(commands.CommandError):
    def __init__(self):
        super().__init__("Text-to-speech messages must be less than 600 characters")

class MissingCredentials(commands.CommandError):
    def __init__(self):
        super().__init__("`Blabby` role or `Manage Channels` permission required when others are in voice channel")

class NotConnected(commands.CommandError):
    def __init__(self):
        super().__init__("You must be in a voice channel to use this command")
