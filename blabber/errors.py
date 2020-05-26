# errors.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Jacky Zhang (jackyeightzhang)
# Date created: 4/3/2020
# Date last modified: 5/24/2020
# Python Version: 3.8.1
# License: MIT License

from discord.ext import commands


class BlabberConnectError(commands.CommandError):
    def __init__(self, message):
        super().__init__(message)

class BlabberNotConnected(BlabberConnectError):
    def __init__(self):
        super().__init__("Blabber is currently not connected to any voice channel")

class BlabberMissingConnectPermission(commands.CommandError):
    def __init__(self, channel_name):
        super().__init__(f"Blabber does not have permission to connect to `{channel_name}`")

class BlabberMissingSpeakPermission(commands.CommandError):
    def __init__(self, channel_name):
        super().__init__(f"Blabber does not have permission to speak in `{channel_name}`")

class BlabberConnectedToAnotherChannel(commands.CommandError):
    def __init__(self):
        super().__init__("Blabber is connected to another voice channel")

class TTSMessageTooLong(commands.CommandError):
    def __init__(self):
        super().__init__("Text-to-speech messages must be less than 600 characters")

class MissingCredentials(commands.CommandError):
    def __init__(self):
        super().__init__("`Blabby` role or `Manage Channels` permission required when others are in voice channel")

class NotConnected(commands.CommandError):
    def __init__(self):
        super().__init__("You must be in a voice channel to use this command")
