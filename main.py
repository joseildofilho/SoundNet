''' Sound Net'''
import time

from Layers.data_link.data_link_layer import DataLink
from Layers.physycal.physical_layer import Physical
from Mediators.physicaldatalinkmediator import PhysicalDataLinkMediator

if '__main__' == __name__:

    data = '101100011011011000110110110001101'

    stack1_physical = Physical()
    stack1_DL = DataLink()
    stack1_physical_dl = PhysicalDataLinkMediator(stack1_DL, stack1_physical)

    stack2_physical = Physical()
    stack2_DL = DataLink()
    stack2_physical_dl = PhysicalDataLinkMediator(stack1_DL, stack1_physical)


