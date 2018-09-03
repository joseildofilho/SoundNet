from asyncio import Queue
from threading import Thread, Lock, Semaphore

import pyaudio
from numpy import fromstring, float64, int16, int32, zeros, float32, pi, arange, sin, int64, log10, array
from numpy.random import rand
from numpy.fft import rfft, irfft, fft

import time

from layer import Layer
from wave_visualizer import WaveVisualizer

import soundcard as sc

from multiprocessing.pool import ThreadPool

LISTENER = sc.default_microphone()

calculate_channel = lambda max_frequency, bit_len: lambda channel: int((bit_len*channel/max_frequency) - 1)

class Physical(Layer):
    '''Physical Layer'''
    def __init__(self):
        Layer.__init__(self)

        self._size_message = 44100

        self._speaker = Speaker(self._size_message, 44100)

        self._listener = Listener(self._size_message//2, 44100)

        self._listener.start()
        time.sleep(3)
        self._speaker.start()

        self._shower = WaveVisualizer('listen', lim=1)
        # self._shower.start()
        self._queue_data = Queue()
    def send_down(self):
        self._gate_down.move_down(self._data)

    def send_up(self):
        self._gate_top.move_up(self._data)

    def receive_up(self, data):
        self._data = data

    def receive_down(self, data):
        self.data = data

    def process_data(self):
        raise NotImplementedError

    def run(self):
        z = zeros(self._size_message)
        self._queue_data.put_nowait('1')
        while True:
            time.sleep(1)
            if not self._queue_data.empty():
                aux = self._queue_data.get_nowait()
                self._speaker.speak(0)
                time.sleep(5)
                for bit in list(aux):
                    if int(bit) == 1:
                        self._speaker.speak(1)
                self._speaker.speak(2)
                self._queue_data.task_done()
            break


class Speaker(Thread):
    def __init__(self, size_message, frame_rate, channels=3, channel_min=1000, channel_max = 9000):
        Thread.__init__(self)

        chan_calc = calculate_channel(channel_max, size_message)
        self._channels = [0 for _ in range(channels)]
        step = (channel_max - channel_min) // (channels - 1)

        aux = zeros(size_message)

        duration = 1.0

        for i in range(channels):
            f = channel_min + step * i
            self._channels[i] = (sin(2 * pi * arange(frame_rate * duration) * f / frame_rate)).astype(float32)
        print(self._channels)
        self._size_message = size_message
        self._frame_rate = frame_rate
        self._paudio = pyaudio.PyAudio()
        self._stream = self._paudio.open(format=pyaudio.paFloat32   ,
                                         channels=1,
                                         rate=frame_rate,
                                         output=True,
                                         frames_per_buffer=size_message)
        self._stream.start_stream()
        self._in = Semaphore(1)
        self._out = Semaphore(0)
        self.data = None


    def speak(self,channel):
        self._in.acquire()
        time.sleep(1)
        self._data = self._channels[channel]
        self._out.release()
    def run(self):
        fill = chr(0)*self._size_message*2
        while True:
            self._out.acquire()
            self._stream.write(fill)
            self._stream.write(self._data)
            self._in.release()

class Listener(Thread):
    def __init__(self, size_message, frame_rate, threshold=0.7, channels=3, channel_min=1000, channel_max=11000):
        Thread.__init__(self)
        self._size_message = size_message
        self._frame_rate = frame_rate
        self._threshold = threshold
        self._channels = zeros(channels,dtype=int64)
        chan_calc = calculate_channel(channel_max, size_message)
        step = channel_max - channel_min
        for i in range(channels):
            self._channels[i] = chan_calc(channel_min + step * i)
        self._channels = array([500,2500,4500])
        self._paudio = pyaudio.PyAudio()
        self._stream = self._paudio.open(format=pyaudio.paInt32,
                                        channels=1,
                                        rate=frame_rate,
                                        input=True,
                                        frames_per_buffer=size_message)
        self._stream.start_stream()
        self._pool = ThreadPool(100)
        self._queuen_in = Queue()

    def listen(self):
        return fromstring(self._stream.read(self._size_message), dtype=int32)

    def run(self):
        code = int64(0)
        while True:
            x = self.listen()
            print('\r' + str(x.max()), end='')
            if x.max() > 2000000000:
                self._pool.apply_async(self._decode(x, code))
                code += 1

    def _decode(self, msg, code):
        print('decoding',code)
        msg = rfft(msg)
        msg /= abs(msg[100:]).max()
        print(msg.argmax())
        for i in abs(msg[self._channels]) > self._threshold:
            if i:
                print('bit', i, abs(msg[self._channels]) > self._threshold, 'code', code, msg.argmax())
                break

class Decoder(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._queue = Queue()
        self._lock = Lock()
