import board
import busio
import digitalio

from .gameduino import Gameduino

class GameduinoCircuitPython(Gameduino):
    def __init__(self):
        self.cs = digitalio.DigitalInOut(board.D8)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.cs.value = True

        self.sd = digitalio.DigitalInOut(board.D9)
        self.sd.direction = digitalio.Direction.OUTPUT
        self.sd.value = True

        self.daz = digitalio.DigitalInOut(board.D10)
        self.daz.direction = digitalio.Direction.OUTPUT
        self.daz.value = True

        self.sp = busio.SPI(board.D13, MOSI=board.D11, MISO=board.D12)
        while not self.sp.try_lock():
            pass
        self.sp.configure(baudrate=15000000, phase=0, polarity=0)

    def controllers(self):
        self.daz.value = False
        bb = bytearray(26)
        self.sp.readinto(bb)
        # print('raw controllers', bb)
        self.daz.value = True

        return (self.wii_classic_pro(bb[2:8]), self.wii_classic_pro(bb[14:20]))

    def transfer(self, wr, rd = 0):
        self.cs.value = False
        self.sp.write(wr)
        if rd == 0:
            self.cs.value = True
        else:
            r = bytearray(rd)
            self.sp.readinto(r)
            self.cs.value = True
            return r
