import time
from threading import Thread, Semaphore

import pyaudio
from numpy import arange, sin, pi, zeros, float32

class Speaker(Thread):
    def __init__(self, size_message, frame_rate):
        Thread.__init__(self)

        self._size_message = size_message
        self._frame_rate = frame_rate

        self._paudio = pyaudio.PyAudio()
        self._stream = self._paudio.open(format=pyaudio.paFloat32,
                                         channels=1,
                                         rate=frame_rate,
                                         output=True,
                                         frames_per_buffer=1)
        self._stream.start_stream()
        self._in = Semaphore(1)
        self._out = Semaphore(0)
        self._data = None

    def speak(self, signal):
        self._in.acquire()
        self._data = signal
        self._out.release()

    def run(self):
        fill = chr(0) * self._size_message * 2
        while True:
            if self._data is None:
                self._stream.write(fill)
            else:
                self._out.acquire()
                self._stream.write(self._data)
                self._in.release()