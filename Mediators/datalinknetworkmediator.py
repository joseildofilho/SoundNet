class DataLinkNetworkMediator:
    def __init__(self, datalink, network):
        self._datalink = datalink
        self._datalink.set_mediator_DL_network(self)
        self._network = network
        self._network.set_mediator_DL_network(self)

    def data_recived(self, data):
        self._network._data_recived(data)

    def send_data(self, data):
        self._datalink._send_data(data)

    def is_ours(self, data):
        return self._network.is_ours(data)
