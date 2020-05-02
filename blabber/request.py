# request.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Jacky Zhang (jackyeightzhang)
# Date created: 1/6/2020
# Date last modified: 5/1/2020
# Python Version: 3.8.1
# License: MIT License

from discord.oggparse import OggStream

from blabber.stream import SimplexIOBase, SimplexReader, SimplexWriter

class TTSRequest(dict):
    """
    Request object that represents a Google Cloud API TTS request.

    attributes:
        message   [str]: text to be converted into audio
        lang_code [str] (default='en-GB'): language code of TTS voice
        name      [str] (default='en-GB-Standard-A'): name of TTS voice
        gender    [str] (default='FEMALE'): gender of TTS voice
    """
    def __init__(
            self,
            message,
            encoding='OGG_OPUS',
            lang_code='en-GB',
            name='en-GB-Standard-A',
            gender='FEMALE'):
        self['audioConfig'] = dict()
        self['input'] = dict()
        self['voice'] = dict()
        # TODO Add support for other audio encodings
        self['audioConfig']['audioEncoding'] = 'OGG_OPUS'
        self['input']['text'] = message
        self['voice']['languageCode'] = lang_code
        self['voice']['name'] = name
        self['voice']['ssmlGender'] = gender


class TTSRequestDispatcher():
    """
    Dispatcher object that submits TTS requests to a handler pool to be
    processed.

    attributes:
        pool [TTSRequestHandlerPool]: handler pool for processing TTS requests
    """
    def __init__(self, pool):
        self._pool = pool
        self._io_base = SimplexIOBase()
        self._ostream = SimplexReader(self._io_base)

    def iter_packets(self):
        """
        Generator used for producing Opus encoded audio packets.

        yields:
            bytes: Opus encoded audio packet
        """
        # Send output stream to OggStream object for Opus packet extraction
        yield from OggStream(self._ostream).iter_packets()

    async def submit_request(self, request):
        """
        Submits a TTS request to the handler pool to be processed.

        parameters:
            request [TTSRequest]: TTS request object to be submitted
        """
        # Spawn a new input stream to write-back response audio data
        istream = SimplexWriter(self._io_base)
        self._pool.submit_job((request, istream))

        # Block until data arrives in IO base object
        await self._ostream.wait_for_data()
