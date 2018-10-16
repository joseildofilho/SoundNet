import pyaudio
from numpy import fromstring, int32


class Listener:
    def __init__(self, size_message=4096, frame_rate=44100):
        self._size_message = size_message
        self._frame_rate = frame_rate
        self._paudio = pyaudio.PyAudio()
        self._stream = self._paudio.open(format=pyaudio.paInt32,
                                         channels=1,
                                         rate=frame_rate,
                                         input=True,
                                         frames_per_buffer=1)
        self._stream.start_stream()

    def listen(self):
        return fromstring(self._stream.read(self._size_message), dtype=int32)