from threading import Thread
import numpy as np
import matplotlib.pyplot as plt

class WaveVisualizer(Thread):
    def __init__(self, name, update_time = 0.001, lim=1):
        Thread.__init__(self)
        self._name = name
        self._lim = lim
        self._update_time = update_time
        self._signal = np.zeros(10)

    def show(self, signal):
        self._signal = signal

    def run(self):
        plt.ion()
        while True:
            plt.plot(self._signal)
            plt.ylim(-self._lim, self._lim)
            plt.title(self._name)
            plt.draw()
            plt.pause(self._update_time)
            plt.gca().cla()