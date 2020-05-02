# audio.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Jacky Zhang (jackyeightzhang)
# Date created: 3/3/2020
# Date last modified: 5/1/2020
# Python Version: 3.8.1
# License: MIT License

from discord.player import AudioSource

from blabber.request import TTSRequestDispatcher

class TTSAudio(AudioSource):
    """
    AudioSource object that streams Opus encoded audio data from TTS request
    responses.
    
    attributes:
        pool [TTSRequestHandlerPool]: handler pool for processing TTS requests
    """
    def __init__(self, pool):
        self._dispatch = TTSRequestDispatcher(pool)
        self._packets = self._dispatch.iter_packets()
        
    def read(self):
        """
        Reads one packet of audio data from the request dispatcher. 
        
        returns:
            bytes: packet of audio data
        """
        try:
            data = next(self._packets)
        except StopIteration:
            data = b''
            # Restart packet iterator
            self._packets = self._dispatch.iter_packets()
        return bytes(data)

    async def submit_request(self, request):
        """
        Submits a TTS request to the request dispatcher to be processed.

        parameters:
            request [TTSRequest]: TTS request object to be submitted
        """
        await self._dispatch.submit_request(request)

    def is_opus(self):
        """
        Query to determine if TTSAudio data is Opus encoded.

        returns:
            bool: value of 'True' if audio data is Opus encoded
        """
        # TODO Add support for other audio encodings
        return True
