import time
import gameduino
from spidriver import SPIDriver

class GameduinoSPIDriver(gameduino.Gameduino):
    def __init__(self):
        # self.d = SPIDriver("/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DO01HE8Q-if00-port0")
        self.d = SPIDriver("/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DO02C71A-if00-port0")

        self.d.unsel()
        self.d.seta(1)
        self.d.setb(1)

        if 1:
            print('reset')
            self.d.setb(0)
            time.sleep(.1)
            self.d.setb(1)

        while 0:
            self.d.unsel()
            self.d.seta(0)
            b = self.d.writeread(b'\x00' * 6)
            self.d.seta(1)
            print(b)

    def controllers(self):
        self.d.seta(0)
        b = self.d.writeread(b'\x00' * 6)
        self.d.seta(1)
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
        return [r, r]

    def transfer(self, wr, rd = 0):
        self.d.sel()
        self.d.write(wr)
        r = self.d.read(rd)
        self.d.unsel()
        return r


