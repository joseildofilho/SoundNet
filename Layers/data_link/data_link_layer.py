import numpy as np
from threading import Thread

from Layers.layer import Layer
from constants import FRAME_SIZE, WORD_SIZE

MESSAGE_START = '101'
MESSAGE_END = '101'

class DataLink(Layer):
    def __init__(self, id):
        Thread.__init__(self)
        self._physical_mediator = None
        self._token = False
        self._id = id
        self._frames_going = []
        self._frames_coming = []
        self._build_frame_buffer = np.array([])

    def set_mediator(self, mediator):
        self._physical_mediator = mediator

    def _send_word(self, word):
        self._physical_mediator.send_word(word)


    def _get_word(self):
        return self._physical_mediator.get_word()

    def send_data(self, data):
        self._frames_going.append(data)

    def get_data(self):
        if self._frames_coming:
            return self._frames_coming.pop(0)

    def _begin_message(self, data):
        if '101' in data:
            return '_begin_message'
        return '_listening_message'

    def _listening_message(self, data):

        if '1010' in data[-4:]:
            self._frame = data[:-1]
            return '_begin_message'

    @staticmethod
    def _validate_frame(frame):
        if frame[:len(MESSAGE_START)] == MESSAGE_START and frame[-len(MESSAGE_END):] == MESSAGE_END:
            return True
        return False

    @staticmethod
    def _remove_message_flag(frame):
        return frame[len(MESSAGE_START): -len(MESSAGE_END)]

    def _token_arrived(self):
        self._token = True
        self._physical_mediator.pause_listen()

    def _token_going(self):
        self._token = False
        self._physical_mediator.start_listen()

    def _protocol(self, frame):
        dl_protocol = frame[0:2]
        frame = frame[2:]
        if (dl_protocol == [0, 0]).all():
            print("reciving token")
            self._token_arrived()
        elif (dl_protocol == [0, 1]).any():
            pass
        return frame
    def _add_frame(self, frame):
        self._frames_going.append(frame)

    def speak_if_have_token(self):
        if self._token:
            for index, frame in enumerate(self._frames_going):
                for word in range(0,FRAME_SIZE, WORD_SIZE):
                    print(word)
                    self._send_word(frame[word:word + WORD_SIZE])
                del self._frames_going[index]
            return True
        return False

    def look_for_frames(self):
        word = self._get_word()
        if word.size and self._build_frame_buffer.size < FRAME_SIZE:
            self._build_frame_buffer = np.concatenate([self._build_frame_buffer, word])
        elif self._build_frame_buffer.size == FRAME_SIZE:
            print('new frame')
            self._build_frame_buffer = DataLink._remove_message_flag(self._build_frame_buffer)
            self._build_frame_buffer = self._protocol(self._build_frame_buffer)
            self._frames_coming.append(self._build_frame_buffer)
            self._build_frame_buffer = np.array([])
        # if word.size != 0 and MESSAGE_START in word:
        #     word = word[word.index(MESSAGE_START):]
        #     for i in range(FRAME_SIZE//WORD_SIZE):
        #         word += self._get_word()
        #     frame = word[:FRAME_SIZE]
        #     print(frame, self._id)
        #     if self._validate_frame(frame):
        #         frame = DataLink._remove_message_flag(frame)
        #         self._protocol(frame)

    def run(self):
        while True:
            if not self.speak_if_have_token():
                self.look_for_frames()
