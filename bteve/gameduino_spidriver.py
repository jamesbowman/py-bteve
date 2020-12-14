import time
import struct
from .gameduino import Gameduino

class GameduinoSPIDriver(Gameduino):
    def __init__(self, d):
        self.d = d

        self.d.unsel()
        self.d.seta(1)
        self.d.setb(1)

        if 0:
            print('reset')
            self.d.setb(0)
            time.sleep(.1)
            self.d.setb(1)

        while 0:
            self.d.sel()
            self.d.unsel()

        while 0:
            self.d.setb(0)
            self.d.setb(1)

        while 0:
            self.d.unsel()
            self.d.seta(0)
            b = self.d.writeread(b'\x00' * 6)
            self.d.seta(1)
            print(b)

        while 0:
            self.d.setb(0)
            b = self.d.writeread(b'\x00' * 24)
            self.d.setb(1)
            print(" ".join(["%02x" % x for x in b]))

        while 0:
            print(self.controllers())

    def dazzler_cmd(self, a, b = 0):
        self.d.setb(0)
        rr = self.d.writeread(struct.pack("BB", a, b))
        self.d.setb(1)
        return struct.unpack("BB", rr)

    def controllers(self):
        self.d.setb(0)
        bb = self.d.writeread(b'\x00' * 26)
        self.d.setb(1)
        return (self.wii_classic_pro(bb[2:8]), self.wii_classic_pro(bb[14:20]))

    def transfer(self, wr, rd = 0):
        self.d.sel()
        self.d.write(wr)
        r = self.d.read(rd)
        self.d.unsel()
        return r
