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