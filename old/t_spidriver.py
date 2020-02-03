import time

class SPI:
    def __init__(self, dev):
    def transfer(self, wr, rd = 0):
        self.d.sel()
        self.d.write(wr)
        r = self.d.read(rd)
        self.d.unsel()
        return r
