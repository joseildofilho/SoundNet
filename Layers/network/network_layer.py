import numpy as np

from Layers.layer import Layer
from constants import ADDRESS_SIZE


class Network(Layer):
    def __init__(self, address):
        self._address = np.array([int(i) for i in address])

        self._data_link = None

        self._buffer = []

    def set_mediator_DL_network(self, mediator):
        self._data_link = mediator

    def data_received(self, data):
        self._buffer.append(data)

    def is_ours(self, data):
        print(data[:ADDRESS_SIZE], self._address)
        print(data[:ADDRESS_SIZE] == self._address)
        return (data[:ADDRESS_SIZE] == self._address).all()

    def send_to(self, address, data):
        address = np.array([int(i) for i in address])
        self._data_link.send_data(np.concatenate([address, data]))

