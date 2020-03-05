# player.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV),
#               Jacky Zhang (jackyeightzhang)
# Date created: 3/3/2020
# Date last modified: 3/3/2020
# Python Version: 3.8.1
# License: MIT License

from discord.player import AudioSource


class TTSAudio(AudioSource):
    """
    AudioSource object used for streaming Opus encoded audio produced by a TTS
    request handler.
    
    attributes:
        handle [TTSRequestHandler]: request handler object containing audio
    """
    def __init__(self, handle):
        self._packets = handle.iter_packets()
        
    def read(self):
        """
        Produces one packet of audio data from underlying TTS request handler.
        
        returns:
            bytes: packet of audio data
        """
        return next(self._packets, b'')

    def is_opus(self):
        """
        Query for determining if AudioSource audio data is Opus encoded.

        returns:
            bool: value of 'True' if audio data is Opus encoded
        """
        # TODO Add support for other audio encodings
        return True
