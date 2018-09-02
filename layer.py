from abc import ABC, abstractmethod
from threading import Thread


class Layer(ABC, Thread):
    '''Abstract class for Layer'''

    def __init__(self):
        Thread.__init__(self)
        self._gate_top = None
        self._gate_down = None
        self._data = None

    @property
    def data(self):
        return self._data

    @data.getter
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @abstractmethod
    def send_down(self):
        raise NotImplementedError

    @abstractmethod
    def send_up(self):
        raise NotImplementedError

    @abstractmethod
    def receive_up(self, data):
        raise NotImplementedError

    @abstractmethod
    def receive_down(self, data):
        raise NotImplementedError

    def set_gate(self, top=None, down=None):
        ''' gaters setter'''
        self._gate_top = top
        self._gate_down = down

    @abstractmethod
    def process_data(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError