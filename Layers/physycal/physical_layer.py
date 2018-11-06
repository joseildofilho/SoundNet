from asyncio import Queue
from threading import Lock, Thread

from numpy import sin, pi, arange, float32
import numpy as np

import sounddevice as sd

from Layers.physycal.physical_encoder import PhysicalEncoder
from Layers.physycal.physical_decoder import Decoder
from Layers.layer import Layer

import time

from constants import FRAME_RATE


class Physical(Layer, Thread):
    '''Physical Layer'''

    def __init__(self, auto_start=True):
        Thread.__init__(self)

        self._data_link_mediator = None

        self._decoder = Decoder()
        self._decoder.pause()
        self._encoder = PhysicalEncoder()

        self._words = []

        self.paused = True

        if auto_start:
            self.start()

    def start_listen(self):
        self._decoder.resume()
        self.paused = False

    def pause_listen(self):
        self._decoder.pause()
        self.paused = True

    def set_mediator(self, mediator):
        self._data_link_mediator = mediator

    def get_word(self):
        if len(self._words) != 0:
            return self._words.pop(0)
        return np.array([])

    def send_word(self, data):
        self._encoder.send(data)

    def _listen(self):
        return sd.rec(FRAME_RATE, channels=1, blocking=True)[:, 0]

    def run(self):
        while True:
            while self.paused:
                time.sleep(2)
            noise = self._listen()
            self._decoder.decode(noise)
            word = self._decoder.get_word()
            if word.size:
                self._words.append(word)