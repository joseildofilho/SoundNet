from threading import Thread
import sounddevice as sd
import numpy as np
import pyaudio as pa
import time
import matplotlib.pyplot as plt

from constants import FRAME_RATE, WORD_SIZE, SIGNAL_PORTER, PHYSICAL_SIGNAL, DURATION


class PhysicalEncoder(Thread):

    _REPEAT = FRAME_RATE//(WORD_SIZE / DURATION)

    def __init__(self):
        Thread.__init__(self)

    def send(self, word):
        x = np.concatenate([PHYSICAL_SIGNAL, np.repeat(word, self._REPEAT) * SIGNAL_PORTER])
        sd.play(x, FRAME_RATE, blocking=True)
