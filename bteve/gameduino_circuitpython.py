import board
import busio
import digitalio

import gameduino

class GameduinoCircuitPython(gameduino.Gameduino):
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
        bb = bytearray(24)
        self.sp.readinto(bb)
        # print('raw controllers', bb)
        self.daz.value = True

        def decode1(b):
            r4 = '. brt b+ bh b- blt bdd bdr'.split()
            r = {id: 1 & (~b[4] >> i) for i,id in enumerate(r4)}
            r5 = 'bdu bdl bzr bx ba by bb bzl'.split()
            r.update({id: 1 & (~b[5] >> i) for i,id in enumerate(r5)})
            r.update({
                'lx' : b[0] & 63,
                'ly' : b[1] & 63,
                'rx' : (((b[0] >> 6) & 3) << 3) |
                       (((b[1] >> 6) & 3) << 1) |
                       (((b[2] >> 7) & 1)),
                'ry' : b[2] & 31,
                'lt' : (((b[2] >> 5) & 3) << 3) |
                       (((b[3] >> 5) & 7)),
                'rt' : b[3] & 31,
            })
            return r

        return (decode1(bb[0:6]), decode1(bb[12:18]))

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
