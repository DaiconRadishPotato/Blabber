# stream.py
#
# Author: Marcos Avila (DaiconV)
# Contributors: Fanny Avila (Fa-Avila),
#               Jacky Zhang (jackyeightzhang)
# Date created: 4/16/2020
# Date last modified: 5/3/2020
# Python Version: 3.8.1
# License: MIT License

import asyncio
import queue
import threading
import time


class SimplexIOBase():
    """
    Uni-directional I/O base object that supports single-read/multi-write
    operations. Attached write accessors are allowed to write in the order of
    their creation.
    """
    def __init__(self):
        # Queue to pass data between accessors
        self.chunks = queue.Queue()

        self._reader = None
        self._writer = None
        self._future_writers = queue.Queue()

        # Internal Lock for synchronized access between threads
        self._lock = threading.Lock()

    def attach_reader(self, reader):
        """
        Attaches a read accessor. Only one read accessor is allowed to attach
        at any given time.

        parameters:
            reader [SimplexReader]: read accessor to attach
        raises:
            IOError: raised when an open read accessor is already attached
        """
        with self._lock:
            # Check if a reader has already been attached
            if self._reader:
                raise IOError('open read accessor already attached')

            self._reader = reader

    def attach_writer(self, writer):
        """
        Attaches a write accessor.

        parameters:
            writer [SimplexWriter]: write accessor to attach
        """
        with self._lock:
            # Check if a writer has been set
            if self._writer:
                # Lock writer and add to FIFO queue
                writer.write_lock.acquire()
                self._future_writers.put(writer)
            else:
                self._writer = writer

    def detach_reader(self, reader):
        """
        Detaches a read accessor.

        parameters:
            reader [SimplexReader]: read accessor to detach
        """
        with self._lock:
            if self._reader is reader:
                self._reader = None

    def detach_writer(self, writer):
        """
        Detaches a write accessor.

        parameters:
            writer [SimplexWriter]: write accessor to detach
        """
        with self._lock:
            if self._writer is writer:
                # Loop through FIFO queue until a valid writer is found
                while not self._future_writers.empty():
                    next_writer = self._future_writers.get()
                    # Check if writer is open
                    if next_writer.is_open():
                        next_writer.write_lock.release()
                        self._writer = next_writer
                        return None

                self._writer = None

    def has_reader(self):
        """
        Query to determine if a read accessor is currently attached.

        returns:
            bool: value of 'True' if a read accessor is attached
        """
        with self._lock:
            return self._reader is not None

    def has_writer(self):
        """
        Query to determine if a write accessor is currently attached.

        returns:
            bool: value of 'True' if a write accessor is attached
        """
        with self._lock:
            return self._writer is not None


class SimplexReader():
    """
    I/O base object accessor with read-only capabilities.

    parameters:
        io_base [SimplexIOBase]: I/O base object to read from
    """
    def __init__(self, io_base):
        self._io_base = io_base
        self._open = True
        self._buffer = bytearray()

        # Internal Lock for synchronized access between threads
        self._lock = threading.Lock()

        # Attach to I/O base object
        io_base.attach_reader(self)

    def __del__(self):
        self.close()

    def is_open(self):
        """
        Query to determine if read accessor is currently open.

        returns:
            bool: value of 'True' if read accessor is open
        """
        with self._lock:
            return self._open

    async def wait_for_data(self):
        """Asynchronous spin-lock to poll I/O base object for data."""
        with self._lock:
            if len(self._buffer) != 0:
                return None

        # Keep polling until data is written to I/O base object
        while self._io_base.chunks.empty():
            await asyncio.sleep(0.05)

    def close(self):
        """Closes read accessor and detaches I/O base object."""
        with self._lock:
            if self._open:
                self._open = False

                # Detatch reader from I/O base object
                self._io_base.detach_reader(self)

    def _readall(self):
        """
        Reads bytes from I/O base object until EOF is reached. Returns an empty
        bytes object when read accessor is at EOF.

        returns:
            bytes: oldest unread data from I/O base object
        """
        # Keep polling until EOF is reached
        while self._io_base.has_writer() or not self._io_base.chunks.empty():
            while not self._io_base.chunks.empty():
                self._buffer += self._io_base.chunks.get()

            # Small sleep before resuming polling loop
            if self._io_base.has_writer():
                time.sleep(0.05)

        # Return data which was read before EOF was reached
        data = self._buffer
        self._buffer = bytearray()
        return bytes(data)

    def read(self, size=-1):
        """
        Reads at most 'size' bytes from I/O base object. If the 'size' argument
        is negative, read until EOF is reached. Returns an empty bytes object
        at EOF.

        parameters:
            size [int] (default=-1): number of bytes to read
        raises:
            ValueError: raised when reading from a closed read accessor
        returns:
            bytes: oldest unread data from attached I/O base object
        """
        # Check if reader is closed
        with self._lock:
            if not self._open:
                raise ValueError('I/O operation on closed accessor')

        # Read until EOF if size parameter is negative
        if size < 0:
            return self._readall()

        # Check if buffer already contains amount of bytes to read
        if len(self._buffer) >= size:
            # Save remaining bytes to buffer
            data = self._buffer[:size]
            self._buffer = self._buffer[size:]
            return bytes(data)

        # Keep polling until enough data has been read or EOF is reached
        while self._io_base.has_writer() or not self._io_base.chunks.empty():
            while not self._io_base.chunks.empty():
                self._buffer += self._io_base.chunks.get()

            # Break out of loop if enough bytes have been read
            if len(self._buffer) >= size:
                data = self._buffer[:size]
                self._buffer = self._buffer[size:]
                return bytes(data)

            # Small sleep before resuming polling loop
            if self._io_base.has_writer():
                time.sleep(0.05)

        # Return data which was read before EOF was reached
        data = self._buffer
        self._buffer = bytearray()
        return bytes(data)

    def readall(self):
        """
        Reads bytes from I/O base object until EOF is reached. Returns an empty
        bytes object when read accessor is at EOF.

        raises:
            ValueError: raised when reading from a closed read accessor
        returns:
            bytes: oldest unread data from attached I/O base object
        """
        # Check if reader is closed
        with self._lock:
            if not self._open:
                raise ValueError('I/O operation on closed accessor')

        return self._readall()


class SimplexWriter():
    """
    I/O base object accessor with write-only capabilities.

    parameters:
        io_base [SimplexIOBase]: I/O base object to write to
    """
    def __init__(self, io_base):
        # Lock to ensure ordered writes to I/O base object
        self.write_lock = threading.Lock()

        self._io_base = io_base
        self._open = True

        # Internal Lock for synchronized access between threads
        self._lock = threading.Lock()

        # Attach to I/O base object
        io_base.attach_writer(self)

    def __del__(self):
        self.close()

    def is_open(self):
        """
        Query to determine if write accessor is currently open.

        returns:
            bool: value of 'True' if write accessor is open
        """
        with self._lock:
            return self._open

    def close(self):
        """Closes write accessor and detaches I/O base object."""
        with self._lock:
            if self._open:
                self._open = False

                # Detatch writer from I/O base object
                self._io_base.detach_writer(self)

    def write(self, data):
        """
        Writes bytes to I/O base object.

        parameters:
            data [bytes]: bytes to be written
        raises:
            ValueError: raised when writing to a closed write accessor
        returns:
            int: number of bytes written to I/O base object
        """
        # Check if writer is closed
        with self._lock:
            if not self._open:
                raise ValueError('I/O operation on closed accessor')

        with self.write_lock:
            self._io_base.chunks.put(data)

        return len(data)
