import pyb
from pyb import Pin

class SPI:
    def __init__(self):
        self.cs = Pin('X5', Pin.OUT_PP)
        self.cs.value(True) # Active low

        if 0:
            pd = Pin('X11', Pin.OUT_PP)
            pd.value(False)
            pd.value(True)

        self.sp = pyb.SPI(1, pyb.SPI.MASTER, baudrate=15000000, polarity=0, phase=0, bits=8, firstbit=pyb.SPI.MSB)

    def transfer(self, wr, rd = 0):
        self.cs.value(False)
        self.sp.send(wr)
        if rd == 0:
            self.cs.value(True)
        else:
            r = bytearray(rd)
            self.sp.recv(r)
            self.cs.value(True)
            return r
