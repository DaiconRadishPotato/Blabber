# request.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Jacky Zhang (jackyeightzhang)
# Date created: 1/6/2019
# Date last modified: 3/9/2020
# Python Version: 3.8.1
# License: MIT License

import asyncio
import base64
import json
import os
import queue
import threading
import time

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

from discord.oggparse import OggStream
from dotenv import load_dotenv


# Retrieve Google API credentials
load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('google_application_credentials')

# Google TTS synthesize speech service endpoint url
SYNTHESIZE_SPEECH = 'https://texttospeech.googleapis.com/v1/text:synthesize'

# Chunk size for response streaming
CHUNK_SIZE = 1024 * 1024


class SimplexStream():
    """Pipe-like stream object used for sending bytes between threads."""
    def __init__(self):
        # Internal queue to pass data between threads
        self._chunks = queue.Queue()
        # Accessor flags to check if read and write objects are open
        self._read_open = False
        self._write_open = False

    def open(self):
        """
        Generates a pair of accessor objects to the SimplexStream;
        reader and writer objects respectively.

        returns:
            SimplexStreamReader: accessor object with read-only permissions
            SimplexStreamWriter: accessor object with write-only permissions
        """
        # Set accessor flags to True to allow read and write access
        self._read_open = True
        self._write_open = True
        # Return a pair of reader and writer objects
        return SimplexStreamReader(self), SimplexStreamWriter(self)

    def close(self):
        """Closes all access to the SimplexStream."""
        self._read_open = False
        self._write_open = False


class SimplexStreamReader():
    """
    SimplexStream accessor object with read-only permission.

    attributes:
        stream [SimplexStream]: stream used for communication between threads
    """
    def __init__(self, stream):
        self._buffer = b''
        self._stream = stream

    def close(self):
        """Closes read access to the SimplexStream."""
        self._stream._read_open = False

    def read(self, size=-1):
        """
        Reads at most size bytes from stream. 
        If the size argument is negative, read until EOF is reached. 
        Returns an empty bytes object at EOF.

        parameters:
            size [int] (default=-1): number of bytes objects to return 
        raises:
            ValueError: raised when reading from a closed file
        returns:
            bytes: oldest unread data
        """
        # Check if reader is closed
        if not self._stream._read_open:
            raise ValueError('I/O operation on closed stream')

        # Check if buffer already contains amount of bytes to read
        if size >= 0 and len(self._buffer) >= size:
            # Save remaining bytes to buffer
            data = self._buffer[:size]
            self._buffer = self._buffer[size:]
            return data

        # Keep polling until enough data has been read or EOF is reached
        data = self._buffer
        while self._stream._write_open or not self._stream._chunks.empty():
            while not self._stream._chunks.empty():
                data += self._stream._chunks.get()

            # Break out of loop if enough bytes have been read
            if size >= 0 and len(data) >= size:
                # Save remaining bytes to buffer
                self._buffer = data[size:]
                data = data[:size]
                break

            # Small sleep before resuming polling loop
            if self._stream._write_open:
                time.sleep(0.01)

        return data


class SimplexStreamWriter():
    """
    SimplexStream accessor object with write-only permission.

    attributes:
        stream [SimplexStream]: stream used for communication between threads
    """
    def __init__(self, stream):
        self._stream = stream

    def close(self):
        """Closes read access to the SimplexStream."""
        self._stream._write_open = False

    def write(self, data):
        """
        Writes bytes to stream.

        parameters:
            data [bytes]: bytes to be written to stream 
        raises:
            ValueError: raised when writing to a closed file
        returns:
            int: number of bytes written to stream
        """
        # Check if writer is closed
        if not self._stream._write_open:
            raise ValueError('I/O operation on closed stream')

        self._stream._chunks.put(data)
        return len(data)


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


class TTSRequestHandler():
    """
    Handler object used for sending and processing a TTS request.
    
    attributes:
        request [TTSRequest]: request object that will be sent
    """
    def __init__(self, request):
        # Initiate a Google Cloud API session
        credentials = service_account.Credentials.from_service_account_file(
            GOOGLE_APPLICATION_CREDENTIALS)
        scoped_credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/cloud-platform'])
        session = AuthorizedSession(scoped_credentials)

        # Create stream objects to send data between threads
        self._ostream, self._istream = SimplexStream().open()

        # Send TTS request through initialized Google Cloud API session
        self._response = session.post(
            SYNTHESIZE_SPEECH, data=json.dumps(request), stream=True)

        # Start thread to extract audio data as it downloads
        audio_producer = threading.Thread(
            target=self._audio_producer, daemon=True)
        audio_producer.start()

    def iter_packets(self):
        """
        Generator used for producing Opus encoded audio packets.

        yields:
            bytes: Opus encoded audio packet
        """
        # Send output stream to OggStream object for Opus packet extraction
        yield from OggStream(self._ostream).iter_packets()

        # Close output stream after processing audio content
        self._ostream.close()

    def _audio_producer(self):
        """Extracts Opus encoded audio data from Google Cloud API response."""
        quote_count = 0
        def extract_b64_audio(data):
            """
            Generator used for extracting base64 encoded audio from a Google
            Cloud API response.
            
            parameters:
                data [bytes]: chunk of raw response data from Google Cloud API
            yields:
                bytes: chunk of extracted base64 encoded audio data
            """
            nonlocal quote_count
            for byte in data:
                # Count number of times a quote character is read
                if byte == ord('"'):
                    quote_count += 1

                # Yield data between 3rd and 4th quote character
                if byte != ord('"') and quote_count == 3:
                    yield byte

        # Iterate through response in chunks for processing
        b64_encoded_prefix = b''
        for chunk in self._response.iter_lines(chunk_size=CHUNK_SIZE):
            b64_encoded_chunk = b64_encoded_prefix + \
                bytes(extract_b64_audio(chunk))

            # Calculate maximum number of bytes to decode (multiple of 4)
            decode_limit = (len(b64_encoded_chunk) // 4) * 4

            # Save remaining bytes to be prefixed to the next chunk
            b64_encoded_prefix = b64_encoded_chunk[decode_limit:]

            # Write decoded chunk to stream
            self._istream.write(base64.b64decode(
                b64_encoded_chunk[:decode_limit]))

        # Close input stream after processing response
        self._istream.close()
