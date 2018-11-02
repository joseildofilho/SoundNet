class DataLinkNetworkMediator:
    def __init__(self, datalink, network):
        self._datalink = datalink
        self._datalink.set_mediator(self)
        self._network = network
        self._network.set_mediator(self)
