import numpy as np
from threading import Thread, Lock

from constants import FRAME_RATE

import matplotlib.pyplot as plt

class Decoder(Thread):
    def __init__(self, visual=False):
        Thread.__init__(self)
        self._visual = visual
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
        self._lock.acquire()
        self._jobs = self._jobs[pad:]
        self._lock.release()

    def _is_enough(self):
        return self._jobs.size > FRAME_RATE * 4

    def _add_word(self, word):
        self._words.append(word)
        print(self._words)

    def _shift_jobs_a_step(self):
        self._lock.acquire()
        self._jobs = self._jobs[self._step:]
        self._lock.release()

    def _decode(self):
        self._filter_signal()
        self._find_word()
        if self._is_enough():
            y = self._jobs[0: self._step]
            y = abs(np.fft.rfft(y))
            if(y[750:850].max() > 9):
                print('bit 1')
                y = self._jobs[self._step: 2*self._step]
                y = abs(np.fft.rfft(y))
                if(y[750:850].max() > 9):
                    print("bit 2, and message")
                    y = []
                    self._shift_jobs_a_step()
                    self._shift_jobs_a_step()
                    for i in range(0, 8):
                        y.append(self._jobs[0: self._step][1950:2050].max())
                        self._shift_jobs_a_step()
                    self._add_word(np.where(np.array(y) > .3, 1, 0))
                else:
                    print("miss value")
                    self._shift_jobs_a_step()
            else:
                self._shift_jobs_a_step()

    def get_word(self):
        if len(self._words) != 0:
            return self._words.pop(0)
        return np.array([])

    def run(self):
        plt.ion()
        print('starting to listen')
        while True:
            if self._jobs.size:
                 self._decode()
            if self._signals:
                self._lock.acquire()
                for _ in range(len(self._signals)):
                    self._jobs = np.concatenate([self._jobs, self._signals.pop(0)])
                if self._visual:
                    plt.gca().cla()
                    plt.plot(self._jobs)
                    plt.ylim(-1,1)
                    plt.show()
                    plt.pause(0.00001)
                self._lock.release()

    def _clear_word_buffer(self):
        self._word_buffer = ""

    def _clear_signal_buffer(self):
        self._lock.acquire()
        self._jobs = np.empty(0)
        self._lock.release()
