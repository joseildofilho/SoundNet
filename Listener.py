import pyaudio
from numpy import fromstring, int32


class Listener:
    def __init__(self, size_message, frame_rate, threshold=0.5, channels=3, channel_min=1000, channel_max=9000):
        self._size_message = size_message
        self._frame_rate = frame_rate
        self._paudio = pyaudio.PyAudio()
        self._stream = self._paudio.open(format=pyaudio.paInt32,
                                         channels=1,
                                         rate=frame_rate,
                                         input=True,
                                         frames_per_buffer=size_message)
        self._stream.start_stream()

    def listen(self):
        return fromstring(self._stream.read(self._size_message), dtype=int32)