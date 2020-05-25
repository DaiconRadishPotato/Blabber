# cache.py
#
# Author:   Jacky Zhang (jackyeightzhang),
#           Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
# Date created: 4/9/2019
# Date last modified: 5/24/2020
# Python Version: 3.8.1
# License: MIT License

import json

from cachetools import TTLCache

from blabber.services import UserService, GuildService


class VoiceProfileCache(TTLCache):
    """
    Voice Profile Cache object that caches recently used voice profiles and 
    removes those that are least frequently used when size limit is reached.

    parameters:
        max_size [int]: maximum size of cache
        time_to_live [int]: time in secs before a cache object expires
    """
    def __init__(self, max_size=500, time_to_live=60):
        super().__init__(maxsize=max_size, ttl=time_to_live)
        self.DEFAULT_VOICE = (
            'voice_97',
            'en-US-Standard-C',
            'FEMALE',
            'en',
            'en-US'
        )
        self._service = UserService()

        with open(r'./blabber/data.json', 'r') as f:
            data = json.load(f)
            self._available_voices = data["voice_info"]

    def __getitem__(self, key):
        """
        Checks if a voice preference is in cache or database and returns it.

        parameters:
            key [tuple]: tuple of discord User and Channel objects
        returns:
            voice_alias [tuple]: tuple of voice information
        """
        voice_alias = super().__getitem__(key)

        if isinstance(voice_alias, str):
            return (voice_alias, *self._available_voices[voice_alias].values())
        elif isinstance(voice_alias, tuple):
            return voice_alias
        else:
            return None

    def __setitem__(self, key, value):
        """
        Creates an voice profile in cache or updates an existing item. Then 
        writes through to the database to ensure consistency.

        parameters:
            key [tuple]: tuple of discord User and Channel objects
            value [str]: string representing a specific alias
        """
        super().__setitem__(key, value)

        if value == self.DEFAULT_VOICE[0]:
            self._service.delete(*key)
        else:
            self._service.insert(*key, value)

    def __missing__(self, key):
        """
        Checks database for voice profile if it does not exist in cache.

        parameter:
            key [tuple]: tuple of discord User and Channel objects
        returns:
            voice [tuple]: dict with voice alias and other voice information
        """
        voice = self._service.select(*key)
        if voice:
            return voice
        else:
            super().__setitem__(key, self.DEFAULT_VOICE[0])
            return self.DEFAULT_VOICE


class PrefixCache(TTLCache):
    """
    Prefix Cache object that caches recently used prefixes and
    removes those that are least recently used when size limit is reached.

    attributes:
        max_size [int]: maximum size of cache
        time_to_live [int]: time in secs before a cache object expires
    """
    def __init__(self, max_size=500, time_to_live=3600):
        super().__init__(maxsize=max_size, ttl=time_to_live)
        self._service = GuildService()
        self.DEFAULT_PREFIX = '>'

    def __setitem__(self, key, value):
        """
        Creates an item in cache or updates an existing item. Then writes
        through to the database to ensure consistency.

        parameters:
            key [Guild]: discord Guild object
            value [str]: string used before commands to invoke blabber bot
        """
        super().__setitem__(key, value)

        if value == self.DEFAULT_PREFIX:
            self._service.delete(key)
        else:
            self._service.insert(key, value)

    def __missing__(self, key):
        """
        Checks database for guild prefix if it does not exist in cache.

        parameter:
            key [Guild]: discord Guild object
        returns:
            prefix [str]: string used for command prefix
        """
        prefix = self._service.select(key)
        if prefix:
            return prefix[0]
        else:
            super().__setitem__(key, self.DEFAULT_PREFIX)
            return self.DEFAULT_PREFIX
