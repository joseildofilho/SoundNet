class PhysicalDataLinkMediator():

    def __init__(self, data_link, physical):
        self._data_link = data_link
        self._data_link.set_mediator(self)

        self._physical = physical
        self._physical.set_mediator(self)

    def send_word(self, data):
        """
        Sends a word, it's means some quantity of *bits*
        :param data: must be a string
        """
        self._physical.send_word(data)

    def get_word(self):
        """
        Listen the medium, for a word size
        :return: a word with the listened bits
        """
        return self._physical.get_word()

    def start_listen(self):
        self._physical.start_listen()

    def pause_listen(self):
        self._physical.pause_listen()