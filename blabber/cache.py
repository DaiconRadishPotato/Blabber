# cache.py
#
# Author:   Jacky Zhang (jackyeightzhang),
#           Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
# Date created: 4/9/2019
# Date last modified: 4/13/2020
# Python Version: 3.8.1
# License: MIT License

from cachetools import TTLCache
from blabber.services import UserService, GuildService

class VoiceProfileCache(TTLCache):
    """
    Voice Profile Cache object that caches recently used voice profiles and 
    removes those that are least frequently used when size limit is reached.

    attributes:
        max_size [int]: maximum size of cache
        time_to_live [int]: time in secs before a cache object expires
    """
    def __init__(self, max_size=500, time_to_live=60):
        super().__init__(maxsize=max_size, ttl=time_to_live)
        self.DEFAULT_VOICE = (
            'voice_1',
            'de-DE-Standard-F',
            'FEMALE',
            'de',
            'de-DE'
        )
        self._service = UserService()


    def __setitem__(self, key, value):
        """
        Creates an item in cache or updates an existing item. Then writes
        through to the database to ensure consistency.

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
        raises:
            NotInDatabase: Does not exist in cache or database. TBD
        """
        voice = self._service.select(*key)
        print(voice)
        if voice is None:
            return None
        else:
            return voice
        

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
        raises:
            NotInDatabase: Does not exist in cache or database. TBD
        """
        prefix = self._service.select(key)
        if prefix is None:
            return None
        else:
            return prefix[0]