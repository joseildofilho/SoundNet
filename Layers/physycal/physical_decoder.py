from threading import Thread

from Layers.physycal.listener import Listener

MESSAGE_IN_OUT_PROTOCOL = '010'

class Decoder(Thread):
    def __init__(self, word=8, tick = 1, border=50, frame_size=44100, frame_rate = 44100, threshold=2000000000, size_buffer=20):
        Thread.__init__(self)

        self._word_size = word

        self._listener = Listener(frame_size)
        self._tick = tick
        self._adjust = 0

        self._border = border
        self.frame_rate = frame_rate

        self._signal_middle = frame_size // 2
        self._signal_down_border = self._signal_middle - self._border
        self._signal_upper_border = self._signal_middle + self._border

        self._threshold = threshold

        self._size_buffer = size_buffer

        self.start()

        self._messages = []

    def _listen(self):
        signal = self._listener.listen()
        return abs(signal[self._signal_down_border: self._signal_upper_border]).max()

    def _decode(self, bit):
        if bit > self._threshold:
            return '1'
        else:
            return '0'
    def get_word(self):
        message = ''
        for i in range(self._word_size):
            bit = self._listen()
            message += self._decode(bit)
            print(message)
        return message
    def run(self):
        message = ''
        print('starting to listen')
        while True:
            bit = self._listen()
            message += self._decode(bit)
            print(message)