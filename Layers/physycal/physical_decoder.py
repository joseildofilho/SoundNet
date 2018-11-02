import numpy as np
from threading import Thread, Lock

from Layers.physycal.listener import Listener
from constants import WORD_SIZE, FRAME_RATE, PHYSICAL_SIGNAL

import sounddevice as sd

import matplotlib.pyplot as plt

class Decoder(Thread):
    def __init__(self):
        Thread.__init__(self)

        self._words = []
        self._jobs = np.array([])
        self._signals = []
        self._lock = Lock()
        self._threshold = 0.3
        self._step = 4000
        self._word_buffer = ""
        self.start()

    def decode(self, bits):
        self._signals.append(bits)

    def _calculate_padding(self):
        padding = np.where(self._jobs != 0)[0]
        if padding.size:
            return padding[0]
        return 0

    def _filter_signal(self):
        self._lock.acquire()
        self._jobs = np.where(abs(self._jobs) > self._threshold, self._jobs, 0)
        self._lock.release()

    def _find_word(self):
        pad = self._calculate_padding()
        self._jobs = self._jobs[pad:]

    def _is_enough(self):
        return self._jobs.size > FRAME_RATE * 4

    def _decode(self):
        self._filter_signal()
        self._find_word()
        if self._is_enough():
            y = self._jobs[0: self._step]
            y = abs(np.fft.rfft(y))
            if(y[750:850].max() > 9):
                y = self._jobs[self._step: 2*self._step]
                y = abs(np.fft.rfft(y))
                if(y[750:850].max() > 9):
                    y = []
                    self._jobs = self._jobs[self._step:]
                    self._jobs = self._jobs[self._step:]
                    for i in range(0, 8):
                        y.append(self._jobs[0: self._step][1950:2050].max())
                        self._jobs = self._jobs[self._step:]
                    print(np.where(np.array(y) > .3, 1, 0))
                else:
                    self._jobs = self._jobs[self._step:]
            else:
                self._jobs = self._jobs[self._step:]

    def get_word(self):
        if len(self._words) != 0:
            return self._words.pop(0)
        return np.array([])

    def run(self):
        print('starting to listen')
        while True:
            if self._jobs.size:
                 self._decode()
            if self._signals:
                for _ in range(len(self._signals)):
                    self._jobs = np.concatenate([self._jobs, self._signals.pop(0)])

    def _clear_word_buffer(self):
        self._word_buffer = ""

    def _clear_signal_buffer(self):
        self._lock.acquire()
        self._jobs = np.empty(0)
        self._lock.release()
