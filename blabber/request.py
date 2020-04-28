# request.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV),
#               Jacky Zhang (jackyeightzhang)
# Date created: 1/6/2019
# Date last modified: 2/14/2020
# Python Version: 3.8.1
# License: MIT License

import asyncio
import base64
import json
import os
import queue
import threading
import time

from discord.oggparse import OggStream
from blabber.stream import SimplexIOBase, SimplexReader, SimplexWriter

class TTSRequest(dict):
    """
    Request object that represents a Google Cloud API TTS request.

    attributes:
        message     [str]: text to be converted into audio
        encoding    [str] (default=OGG_OPUS): encoding type for audio
        gender      [str] (default=NEUTRAL): gender of TTS speaker
        region_code [str] (default=en-US): region of TTS speaker
    """
    def __init__(
            self,
            message,
            encoding='OGG_OPUS',
            gender='NEUTRAL',
            region_code='en-US'):
        self['audioConfig'] = dict()
        self['input'] = dict()
        self['voice'] = dict()
        # TODO Add support for other audio encodings
        self['audioConfig']['audioEncoding'] = 'OGG_OPUS'
        # self['audioConfig']['audioEncoding'] = encoding
        self['input']['text'] = message
        self['voice']['ssmlGender'] = gender
        self['voice']['languageCode'] = region_code


class TTSRequestManager():
    def __init__(self, pool):
        # Create stream objects to send data between threads
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

    def submit_request(self, request):
        """
        Spawns a thread to handle a TTS request.

        parameters:
            request [TTSRequest]: request object that will be sent
        """
        istream = SimplexWriter(self._io_base)
        self._pool.submit_job((request, istream))
