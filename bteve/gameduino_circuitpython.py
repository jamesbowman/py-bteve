import os
import board
import busio
import digitalio

from .gameduino import Gameduino

class GameduinoCircuitPython(Gameduino):
    def __init__(self):
        if os.uname().machine == 'Raspberry Pi Pico with rp2040':
            self.sp = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)
            cs = (board.GP5, board.GP6, board.GP7)
        else:
            self.sp = busio.SPI(board.D13, MOSI=board.D11, MISO=board.D12)
            cs = (board.D8, board.D9, board.D10)
        def pin(p):
            r = digitalio.DigitalInOut(p)
            r.direction = digitalio.Direction.OUTPUT
            r.value = True
            return r
        (self.cs, self.sd, self.daz) = [pin(p) for p in cs]
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
