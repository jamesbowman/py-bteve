import board
import busio
import digitalio

class SPI:
    def __init__(self):
        self.cs = digitalio.DigitalInOut(board.D2)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.cs.value = True

        self.sp = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        while not self.sp.try_lock():
            pass
        self.sp.configure(baudrate=10000000, phase=0, polarity=0)

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
