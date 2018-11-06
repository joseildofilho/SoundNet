''' Sound Net'''
import numpy as np
import time

from Layers.data_link.data_link_layer import DataLink
from Layers.network.network_layer import Network
from Layers.physycal.physical_layer import Physical
from Mediators.datalinknetworkmediator import DataLinkNetworkMediator
from Mediators.physicaldatalinkmediator import PhysicalDataLinkMediator
from constants import FRAME_SIZE, MESSAGE_END, MESSAGE_START

if '__main__' == __name__:


    data = np.random.randint(0, 2, 22)
    print('transmiting: %s\nlen: %i' % (data, len(data)))

    stack1_physical = Physical()
    stack1_DL = DataLink(1)
    stack1_network = Network('01')

    stack1_physical_dl = PhysicalDataLinkMediator(stack1_DL, stack1_physical)
    stack1_DL_network = DataLinkNetworkMediator(stack1_DL, stack1_network)

    stack1_DL.start()

    stack1_DL._token_going()

    print('sending to 00')
    stack1_network.send_to('00', data)

