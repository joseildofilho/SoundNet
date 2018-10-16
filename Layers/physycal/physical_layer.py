from asyncio import Queue
from threading import Lock, Thread

from numpy import sin, pi, arange, float32

import time

from Layers.physycal.speaker import Speaker
from Layers.physycal.physical_decoder import Decoder
from Layers.layer import Layer

def calculate_channel(max_frequency, bit_len):
    return lambda channel: int((bit_len * channel / max_frequency) - 1)


FRAME_RATE = 44100
FREQ = 200
DURATION = 1

SIGNAL = (sin(2 * pi * arange(FRAME_RATE * DURATION) * FREQ / FRAME_RATE)).astype(float32)


class Physical(Layer, Thread):
    '''Physical Layer'''

    def __init__(self, auto_start=True):
        Thread.__init__(self)

        self._data_link_mediator = None

        self._speaker = Speaker()
        self._decoder = Decoder(tick=DURATION)

        self._queue_data = Queue()

        self._entry_lock = Lock()

        if auto_start:
            self.start()

    def set_mediator(self, mediator):
        self._data_link_mediator = mediator

    def get_word(self):
        return self._decoder.get_word()

    def send_word(self, data):
        self._process_data(data)

    def _process_data(self, data):
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
