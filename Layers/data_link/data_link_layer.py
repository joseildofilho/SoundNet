from Layers.layer import Layer


class DataLink(Layer):
    def __init__(self):
        self._physical_mediator = None

    def set_mediator(self, mediator):
        self._physical_mediator = mediator

    def _send_word(self, word):
        self._physical_mediator.send_word(word)

    def _get_word(self):
        return self._physical_mediator.get_word()

