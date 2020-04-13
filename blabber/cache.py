# cache.py
#
# Author:   Jacky Zhang (jackyeightzhang),
#           Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
# Date created: 4/9/2019
# Date last modified: 4/13/2020
# Python Version: 3.8.1
# License: MIT License

from cachetools import LFUCache, LRUCache

class VoiceProfileCache(LFUCache):
    """
    Voice Profile Cache object that caches recently used voice profiles and 
    removes those that are least frequently used when size limit is reached.
    """
    def init(self, maxsize):
        # initialize database connection
        super().init(max_size)

    def getitem(self, key):
        try:
              value = super().getitem(key)
        except KeyError as e:
            # read from database
            if value == None:
                raise e

        return value

    def setitem(self, key, value):
        super().setitem(key, value)
        # write to database


class PrefixCache(LRUCache):
    """
    Prefix Cache object that caches recently used prefixes and
    removes those that are least recently used when size limit is reached.
    """
    def init(self, maxsize):
        # initialize database connection
        super().init(max_size)

    def getitem(self, key):
        try:
              value = super().getitem(key)
        except KeyError as e:
            # read from database
            if value == None:
                raise e

        return value

    def setitem(self, key, value):
        super().setitem(key, value)
        # write to database
