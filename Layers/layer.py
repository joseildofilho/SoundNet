from abc import ABC, abstractmethod
from threading import Thread


class Layer(ABC, Thread):
    '''Abstract class for Layer'''

    def __init__(self):
        pass
