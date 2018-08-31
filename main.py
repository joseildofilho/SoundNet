from abc import ABC, abstractmethod

class Layer(ABC):
    '''Abstract class for Layer'''

    def __init__(self):
        self._gate_top = None
        self._gate_down = None
        self._data = None

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

    @abstractmethod
    def set_gate(self, top=None, down=None):
        ''' gaters setter'''
        raise NotImplementedError
    
    @abstractmethod
    def process_data(self):
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

    def send_down(self):
        raise NotImplementedError

    def send_up(self):
        raise NotImplementedError

    def receive_up(self, data):
        raise NotImplementedError

    def receive_down(self, data):
        raise NotImplementedError

    def set_gate(self, top=None, down=None):
        raise NotImplementedError
    
    def process_data(self):
        raise NotImplementedError

