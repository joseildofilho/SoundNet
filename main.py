from abc import ABC, abstractmethod
from threading import Thread
from _thread import start_new_thread

class Data:
    def __init__(self):
        self.header = ""
        self.data = ""
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

class Gate():

    def __init__(self, layer_top, layer_down):
        self._top = layer_top
        self._top.set_gate(down=self)

        self._down = layer_down
        self._down.set_gate(top=self)

    def move_down(self, data):
        self._down.receive_top(data)

    def move_top(self, data):
        self._top.receive_down(data)

class Physical(Layer):
    '''Physical Layer'''
    def __init__(self, channel):
        Layer.__init__(self)

        self._channel = channel

    def send_down(self):
        self._gate_down.move_down(self._data)

    def send_up(self):
        self._gate_top.move_up(self._data)

    def receive_up(self, data):
        self._data = data

    def receive_down(self, data):
        self.data = data

    def process_data(self):
        raise NotImplementedError

    def run(self):
        start_new_thread(self._listen, ('Physical Listener', 1))
        start_new_thread(self._speak, ('Physical Speaker', 1))
        while True:
            pass
    def _listen(self, thread_name, delay):
        raise NotImplementedError

    def _speak(self, thread_name, delay):
        raise NotImplementedError
if '__main__' == __name__:
    layer = Physical()
    layer.data = Data()
    layer.start()

