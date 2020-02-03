import time
from spidriver import SPIDriver

class SPI:
    def __init__(self, dev):
        self.d = SPIDriver(dev)

        self.d.unsel()
        self.d.seta(1)
        self.d.setb(1)
        print('reset')
        self.d.setb(0)
        time.sleep(.1)
        self.d.setb(1)

    def transfer(self, wr, rd = 0):
        self.d.sel()
        self.d.write(wr)
        r = self.d.read(rd)
        self.d.unsel()
        return r
