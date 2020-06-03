# errors.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Jacky Zhang (jackyeightzhang)
# Date created: 4/3/2020
# Date last modified: 5/29/2020
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
        super().__init__(f"Blabber does not have `Connect` permission in `{channel_name}`")


class BlabberMissingSpeakPermission(commands.CommandError):
    def __init__(self, channel_name):
        super().__init__(f"Blabber does not have `Speak` permission in `{channel_name}`")


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


class VoiceNotSupported(commands.CommandError):
    def __init__(self, alias):
        super().__init__(f"`{alias}` is not a supported voice")
 

class GenderNotSupported(commands.CommandError):
    def __init__(self, gender):
        super().__init__(f"`{gender}` is not a supported gender")


class LanguageNotSupported(commands.CommandError):
    def __init__(self, language):
        super().__init__(f"`{language}` is not a supported language")


class InvalidPrefix(commands.CommandError):
    def __init__(self, prefix):
        super().__init__(f"`{prefix}` is not a valid prefix")
