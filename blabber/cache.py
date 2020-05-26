# cache.py
#
# Author:   Jacky Zhang (jackyeightzhang),
#           Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
# Date created: 4/9/2019
# Date last modified: 5/5/2020
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
        self.DEFAULT_VOICE = 'voice_92'
        self._service = UserService()

    def __setitem__(self, key, value):
        """
        Creates an voice profile in cache or updates an existing item. Then 
        writes through to the database to ensure consistency.

        parameters:
            key [tuple]: tuple of discord User and Channel objects
            value [str]: string representing a specific alias
        """
        super().__setitem__(key, value)

        if value == self.DEFAULT_VOICE:
            self._service.delete(*key)
        else:
            self._service.insert(*key, value)

    def __missing__(self, key):
        """
        Checks database for voice profile if it does not exist in cache.

        parameter:
            key [tuple]: tuple of discord User and Channel objects
        returns:
            str: voice alias
        """
        row = self._service.select(*key)
        if row:
            value = row[0]
        else:
            value = self.DEFAULT_VOICE

        super().__setitem__(key, value)

        return value


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
            key [tuple]: tuple of discord User and Channel objects
        returns:
            str: string used for command prefix
        """
        row = self._service.select(key)
        if row:
            value = row[0]
        else:
            value = self.DEFAULT_PREFIX

        super().__setitem__(key, value)

        return value
