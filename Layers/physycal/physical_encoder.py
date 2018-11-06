from threading import Thread
import sounddevice as sd
import numpy as np
import time

from constants import FRAME_RATE, WORD_SIZE, SIGNAL_PORTER, PHYSICAL_SIGNAL, DURATION


class PhysicalEncoder(Thread):

    _REPEAT = FRAME_RATE//(WORD_SIZE / DURATION)

    def __init__(self):
        pass

    def send(self, word):
        print("sending word:", word)
        time.sleep(1)
        x = np.concatenate([PHYSICAL_SIGNAL, np.repeat(word, self._REPEAT) * SIGNAL_PORTER])
        sd.play(x, FRAME_RATE, blocking=True)
