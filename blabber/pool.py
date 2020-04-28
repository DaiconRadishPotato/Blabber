# pool.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV),
#               Jacky Zhang (jackyeightzhang)
# Date created: 4/20/2020
# Date last modified: 2/14/2020
# Python Version: 3.8.1
# License: MIT License

import base64
import json
import os
import queue
import threading

from collections.abc import Generator
from dotenv import load_dotenv
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

# Retrieve Google API credentials
load_dotenv()
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('google_application_credentials')

# Google TTS synthesize speech service end-point url
SYNTHESIZE_SPEECH = 'https://texttospeech.googleapis.com/v1/text:synthesize'

# Chunk size for response streaming
CHUNK_SIZE = 1024 * 1024

# Number of handler thread running in pool
REQUEST_HANDLER_COUNT = 50


class TTSRequestHandler(threading.Thread):
    """
    Handler object used for sending and processing a TTS request.
    
    attributes:
        request [TTSRequest]: request object that will be sent
    """
    def __init__(self, jobs, session):
        threading.Thread.__init__(self)
        self.daemon = True
        self._jobs = jobs
        self._session = session

        self._quote_count = 0
        
    def _extract_b64_data(self, data):
        """
        Generator used for extracting base64 encoded audio from a Google
        Cloud API response.

        parameters:
            data [bytes]: chunk of raw response data from Google Cloud API
        """
        for byte in data:
            # Count number of times a quote character is read
            if byte == ord('"'):
                self._quote_count += 1

            # Yield data between 3rd and 4th quote character
            if byte != ord('"') and self._quote_count == 3:
                yield byte

    def run(self):
        """Extracts Opus encoded audio data from Google Cloud API response."""

        while True:
            self._quote_count = 0
            # Remain idle until a job is retrieved
            request, istream = self._jobs.get()
            # Send TTS request through Google Cloud API session
            response = self._session.post(
                SYNTHESIZE_SPEECH, data=json.dumps(request), stream=True)

            # Iterate through response in chunks for processing
            b64_encoded_prefix = b''
            for chunk in response.iter_lines(chunk_size=CHUNK_SIZE):
                b64_encoded_chunk = b64_encoded_prefix + \
                    bytes(self._extract_b64_data(chunk))

                # Calculate maximum number of bytes to decode (multiple of 4)
                decode_limit = (len(b64_encoded_chunk) // 4) * 4

                # Save remaining bytes to be prefixed to the next chunk
                b64_encoded_prefix = b64_encoded_chunk[decode_limit:]

                # Write decoded chunk to stream
                istream.write(base64.b64decode(
                    b64_encoded_chunk[:decode_limit]))

            # Close input stream after processing response
            istream.close()


class TTSRequestHandlerPool():
    def __init__(self, handler_count=50):
        self._jobs = queue.Queue()
        self._handlers = [None] * handler_count
        
        # Initiate a Google Cloud API session
        credentials = service_account.Credentials.from_service_account_file(
            GOOGLE_APPLICATION_CREDENTIALS)
        scoped_credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/cloud-platform'])
        self._session = AuthorizedSession(scoped_credentials)

        for index in range(handler_count):
            self._handlers[index] = TTSRequestHandler(self._jobs, self._session)
            self._handlers[index].start()

    def submit_job(self, job):
        self._jobs.put(job)
