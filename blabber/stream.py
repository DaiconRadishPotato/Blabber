# stream.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Marcos Avila (DaiconV),
#               Jacky Zhang (jackyeightzhang)
# Date created: 4/16/2020
# Date last modified: 4/24/2020
# Python Version: 3.8.1
# License: MIT License

import queue
import threading
import time

class SimplexIOBase():
    """
    Uni-directional stream object that supports single-read/multi-write
    operations. Write accessors are allowed to write in the order of their 
    creation.
    """
    def __init__(self):
        # Internal queue to pass data between threads
        self._chunks = queue.Queue()

        self._lock = threading.Lock()
        self._reader = None
        self._writer = None
        self._future_writers = queue.Queue()

    def _add_reader(self, reader):
        with self._lock:
            if self._reader:
                raise IOError('open read accessor already exists')

            self._reader = reader

    def _add_writer(self, writer):
        with self._lock:
            if self._writer:
                writer._write_lock.acquire()
                self._future_writers.put(writer)
            else:
                self._writer = writer

    def _remove_reader(self, reader):
        with self._lock:
            if self._reader is reader:
                self._reader = None

    def _remove_writer(self, writer):
        with self._lock:
            if self._writer is writer:
                self._writer = None
            
                while self._writer == None:
                    if self._future_writers.empty():
                        break

                    next_writer = self._future_writers.get()
                    if not next_writer.is_open():
                        continue

                    next_writer._write_lock.release()
                    self._writer = next_writer

    def has_reader(self):
        with self._lock:
            return self._reader != None

    def has_writer(self):
        with self._lock:
            return self._writer != None

class SimplexReader():
    """
    SimplexIOBase accessor object with read-only permission.

    attributes:
        stream [SimplexStream]: SimplexStream object to read from
    """
    def __init__(self, raw):
        self._raw = raw
        self._lock = threading.Lock()

        self._open = True
        self._buffer = bytearray()
        
        raw._add_reader(self)
    
    def __del__(self):
        self.close()

    # Queries
    def is_open(self):
        with self._lock:
            return self._open

    # Commands
    def close(self):
        """Closes read access to the SimplexStream."""
        with self._lock:
            if self._open:
                self._open = False
                self._raw._remove_reader(self)

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
        print("read called!")
        # Check if reader is closed
        with self._lock:
            if not self._open:
                raise ValueError('I/O operation on closed stream')

            if size < 0:
                return self.readall()

            # Check if buffer already contains amount of bytes to read
            if len(self._buffer) >= size:
                # Save remaining bytes to buffer
                data = self._buffer[:size]
                self._buffer = self._buffer[size:]
                print("size: " + str(size))
                print(data)
                return bytes(data)

            # Keep polling until enough data has been read or EOF is reached
            while self._raw.has_writer() or not self._raw._chunks.empty():
                while not self._raw._chunks.empty():
                    self._buffer += self._raw._chunks.get()

                # Break out of loop if enough bytes have been read
                if len(self._buffer) >= size:
                    data = self._buffer[:size]
                    self._buffer = self._buffer[size:]
                    print("size: " + str(size))
                    print(data)
                    return bytes(data)

                # Small sleep before resuming polling loop
                if self._raw.has_writer():
                    time.sleep(0.01)

            print("nada")
            return bytes(b'')

    def readall(self):
        while self._raw.has_writer() or not self._raw._chunks.empty():
            while not self._raw._chunks.empty():
                self._buffer += self._raw._chunks.get()
        
            if self._raw.has_writer():
                time.sleep(0.01)

        data = self._buffer
        self._buffer = bytearray()
        return bytes(data)



class SimplexWriter():
    """
    SimplexStream accessor object with write-only permission.

    attributes:
        stream [SimplexStream]: SimplexStream object to write to
    """
    def __init__(self, raw):
        self._raw = raw
        self._lock = threading.Lock()
        self._write_lock = threading.Lock()

        self._open = True

        raw._add_writer(self)

    def __del__(self):
        self.close()

    # Queries
    def is_open(self):
        with self._lock:
            return self._open
    
    # Commands
    def close(self):
        """Closes read access to the SimplexStream."""
        with self._lock:
            if self._open:
                self._open = False
                self._raw._remove_writer(self)

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
        with self._lock:
            if not self._open:
                raise ValueError('I/O operation on closed stream')

        with self._write_lock:
            self._raw._chunks.put(data)
        return len(data)

