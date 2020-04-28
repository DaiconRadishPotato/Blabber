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
from blabber.request import TTSRequestManager

class TTSAudio(AudioSource):
    """
    AudioSource object used for streaming Opus encoded audio produced by a TTS
    request handler.
    
    attributes:
        handle [TTSRequestHandler]: request handler object containing audio
    """
    def __init__(self, pool):
        self._manager = TTSRequestManager(pool)
        self._packets = self._manager.iter_packets()
        
    def read(self):
        """
        Produces one packet of audio data from underlying TTS request handler.
        
        returns:
            bytes: packet of audio data
        """
        try:
            data = next(self._packets)
        except StopIteration:
            data = b''
            self._packets = self._manager.iter_packets()
        return data

    def submit_request(self, request):
        self._manager.submit_request(request)

    def is_opus(self):
        """
        Query for determining if AudioSource audio data is Opus encoded.

        returns:
            bool: value of 'True' if audio data is Opus encoded
        """
        # TODO Add support for other audio encodings
        return True
