from asyncio import Queue
from threading import Thread, Lock, Semaphore

import pyaudio
from numpy import fromstring, float64, int16, zeros, float32, pi, arange, sin
from numpy.random import rand
from numpy.fft import rfft, irfft

import time

from layer import Layer
from wave_visualizer import WaveVisualizer

import soundcard as sc

LISTENER = sc.default_microphone()

class Physical(Layer):
    '''Physical Layer'''
    def __init__(self, channel):
        Layer.__init__(self)

        self._channel = channel
        self._size_message = 44100
        self._speaker = Speaker(self._size_message, self._size_message)
        self._speaker.start()
        self._listener = Listener(self._size_message, self._size_message, channels=[self._size_message//4])
        self._listener.start()
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
        z = zeros(self._size_message//2 + 1)
        z[self._size_message//2] = 100000000
        z = irfft(z)
        print(z.shape)
        while True:
            # x = rfft(self._listener.listen())
            # x /= abs(x).max()
            # #self._shower.show(x)
            # if x[self._size_message//2] > 0.7:
            #    print('1')
            #    time.sleep(0.5)
            self._speaker.speak(z)
            break


class Speaker(Thread):
    def __init__(self, size_message, frame_rate):
        Thread.__init__(self)
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
    def speak(self, data):
        self._in.acquire()
        self._data = data
        self._out.release()
    def run(self):
        fill = chr(0)*self._size_message*2
        while True:
            while not self._out.acquire(blocking=False):
                #print('filling in')
                self._stream.write(fill)
            print('speaking')
            self._stream.write(self._data)
            self._in.release()


class Listener(Thread):
    def __init__(self, size_message, frame_rate, threshold=0.3, channels = []):
        Thread.__init__(self)
        self._size_message = size_message
        self._frame_rate = frame_rate
        self._threshold = threshold
        self._channels = channels
        self._paudio = pyaudio.PyAudio()
        self._stream = self._paudio.open(format=pyaudio.paInt16,
                                        channels=1,
                                        rate=frame_rate,
                                        input=True,
                                        frames_per_buffer=size_message)
        self._stream.start_stream()
    def listen(self):
        return fromstring(self._stream.read(self._size_message), dtype=int16)
    def run(self):
        w = WaveVisualizer('a')
        w.start()
        while True:
            x = rfft(self.listen()).astype(float64)
            x /= abs(x).max()
            print(x[1000:].argmax())
            for i in abs(x[self._channels]) > self._threshold:
                print('bit', i)


