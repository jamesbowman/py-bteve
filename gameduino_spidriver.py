import time
import gameduino
from spidriver import SPIDriver

class GameduinoSPIDriver(gameduino.Gameduino):
    def __init__(self):
        self.d = SPIDriver("/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DO01HE8Q-if00-port0")

        self.d.unsel()
        self.d.seta(1)
        self.d.setb(1)
        if 0:
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


