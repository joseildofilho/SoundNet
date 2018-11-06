import numpy as np

WORD_SIZE = 8
FRAME_SIZE = 32
FRAME_RATE = 20000
FREQUENCY = 200
DURATION = 0.8
PHYSICAL_SIGNAL_DARATION = 0.2

MESSAGE_START = np.array([1, 0, 1])
MESSAGE_END = np.array([1, 0, 1])

PHYSICAL_SIGNAL = np.sin(2 * np.pi * np.arange(FRAME_RATE * PHYSICAL_SIGNAL_DARATION) * 4 * FREQUENCY / FRAME_RATE) * 10
SIGNAL_PORTER = np.sin(2 * np.pi * np.arange(FRAME_RATE * DURATION) * FREQUENCY / FRAME_RATE) * 1000
