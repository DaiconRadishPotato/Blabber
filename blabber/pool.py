# pool.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Jacky Zhang (jackyeightzhang)
# Date created: 4/20/2020
# Date last modified: 5/3/2020
# Python Version: 3.8.1
# License: MIT License

import base64
import json
import os
import queue
import threading

from dotenv import load_dotenv
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

load_dotenv()

# Chunk size for response streaming
CHUNK_SIZE = 1024 * 1024

# Number of handler threads running in handler pool
HANDLER_COUNT = 100


class TTSRequestHandler(threading.Thread):
    """
    Handler thread which processes TTS request jobs from a handler pool and
    writes response audio data to input stream provided in TTS request job.

    parameters:
        pool [TTSRequestHandlerPool]: handler pool from which handler thread
                                      spawned from
    """
    def __init__(self, pool):
        super().__init__()

        self._session = pool._session
        self._terminate = pool._terminate
        self._jobs = pool._jobs

    def _extract_b64_data(self, data):
        """
        Generator used for extracting base64 encoded data from a Google Cloud
        API response.

        parameters:
            data [bytes]: chunk of raw response data
        yields:
            int: integer representation of a byte of base64 encoded data
        """
        quote_count = 0
        for byte in data:
            # Count number of times a quote character is read
            if byte == ord('"'):
                quote_count += 1

            # Yield data between 3rd and 4th quote character
            if byte != ord('"') and quote_count == 3:
                yield byte

    def run(self):
        """Running loop for handler thread object."""
        # Keep polling job queue
        while not self._terminate.is_set():
            # Attempt to retrieve a job
            try:
                job = self._jobs.get(timeout=1)
            except queue.Empty:
                continue

            request, istream = job
            extract_b64_data = self._extract_b64_data
            try:
                # Send TTS request through Google Cloud API session
                response = self._session.post(
                    'https://texttospeech.googleapis.com/v1/text:synthesize',
                    data=json.dumps(request), stream=True)

                # Verify if request succeded
                if not response.ok:
                    continue

                # Iterate through response in chunks for processing
                b64_encoded_prefix = bytearray()
                for chunk in response.iter_lines(chunk_size=CHUNK_SIZE):
                    b64_encoded_chunk = (b64_encoded_prefix
                                         + bytes(extract_b64_data(chunk)))

                    # Calculate maximum number of bytes to decode
                    decode_limit = (len(b64_encoded_chunk) // 4) * 4

                    # Save remaining bytes to be prefixed to the next chunk
                    b64_encoded_prefix = b64_encoded_chunk[decode_limit:]

                    # Write decoded chunk to stream
                    istream.write(base64.b64decode(
                        b64_encoded_chunk[:decode_limit]))
            finally:
                # Close input stream after processing response
                istream.close()


class TTSRequestHandlerPool():
    """Handler pool for processing TTS request jobs."""
    def __init__(self):
        # Initialize Google Cloud API session
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv('google_application_credentials'))
        scoped_credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/cloud-platform'])
        self._session = AuthorizedSession(scoped_credentials)

        self._terminate = threading.Event()
        self._jobs = queue.Queue()
        self._handlers = [None] * HANDLER_COUNT

        # Spawn handler threads
        for index in range(HANDLER_COUNT):
            self._handlers[index] = TTSRequestHandler(self)
            self._handlers[index].start()

    def __del__(self):
        self.teardown()

    def submit_job(self, job):
        """
        Submits a TTS request job to a FIFO job queue for processing.

        parameters:
            job [(TTSRequest, SimplexWriter)]: TTS request job to be submitted
        """
        self._jobs.put(job)

    def teardown(self):
        """Terminates all active handler threads in handler pool."""
        # Check if teardown has already been performed
        if not self._terminate.is_set():
            # Set termination flag
            self._terminate.set()

            # Join all handler threads
            for handler in self._handlers:
                handler.join()
