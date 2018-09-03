''' Sound Net'''

from physical_layer import Physical

class Data:
    def __init__(self):
        self.header = ""
        self.data = ""


if '__main__' == __name__:
    #listener = Listener(1000,44100)
    #print(listener.listen())
    layer = Physical()
    layer.data = Data()
    layer.start()

