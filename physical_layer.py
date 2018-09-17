from asyncio import Queue
from threading import Lock

from numpy import sin, pi, arange, float32

import time

from speaker import Speaker
from physical_decoder import Decoder
from layer import Layer

import soundcard as sc

LISTENER = sc.default_microphone()


def calculate_channel(max_frequency, bit_len):
    return lambda channel: int((bit_len * channel / max_frequency) - 1)


FRAME_RATE = 44100
FREQ = 200
DURATION = 1

SIGNAL = (sin(2 * pi * arange(FRAME_RATE * DURATION) * FREQ / FRAME_RATE)).astype(float32)


class Physical(Layer):
    '''Physical Layer'''

    def __init__(self, auto_start=True):
        Layer.__init__(self)

        self._speaker = Speaker()
        self._decoder = Decoder(tick=DURATION)

        self._queue_data = Queue()

        self._entry_lock = Lock()

        if auto_start:
            self.start()

    def send_down(self):
        self._gate_down.move_down(self._data)

    def send_up(self):
        self._gate_top.move_up(self._data)

    def receive_up(self, data):
        self._data = data

    def receive_down(self, data):
        self.data = data

    def process_data(self, data):
        self._entry_lock.acquire()
        self._queue_data.put_nowait(data)
        self._entry_lock.release()

    def run(self):
        while True:
            if not self._queue_data.empty():
                aux = self._queue_data.get_nowait()
                print('Starting to send: %s' % aux)
                for sig in aux:
                    if int(sig):
                        self._speaker.speak(SIGNAL)
                    time.sleep(DURATION)
                self._queue_data.task_done()
