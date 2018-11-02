''' Sound Net'''
import numpy as np
import time

from Layers.data_link.data_link_layer import DataLink
from Layers.physycal.physical_layer import Physical
from Mediators.physicaldatalinkmediator import PhysicalDataLinkMediator
from constants import FRAME_SIZE, MESSAGE_END, MESSAGE_START

if '__main__' == __name__:


    data = np.concatenate([MESSAGE_START,
                           np.random.randint(0,2,FRAME_SIZE - len(MESSAGE_START) - len(MESSAGE_END)),
                           MESSAGE_END], axis=None,)
    print('transmiting: %s\nlen: %i' % (data, len(data)))
    stack1_physical = Physical()
    stack1_DL = DataLink(1)
    stack1_physical_dl = PhysicalDataLinkMediator(stack1_DL, stack1_physical)
    stack1_DL.start()

    # stack2_physical = Physical()
    # stack2_DL = DataLink(2)
    # stack2_physical_dl = PhysicalDataLinkMediator(stack2_DL, stack2_physical)
    # stack2_DL.start()


    stack1_DL._token = True
    time.sleep(1)
#    stack1_DL.send_data(data)

