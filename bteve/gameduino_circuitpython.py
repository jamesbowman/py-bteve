import os
import board
import busio
import digitalio
import sdcardio
import storage

from .gameduino import Gameduino

def spilock(f):
    def wrapper(*args):
        spi = args[0].sp
        while not spi.try_lock():
            pass
        r = f(*args)
        spi.unlock()
        return r
    return wrapper

class GameduinoCircuitPython(Gameduino):
    def __init__(self):
        mach = os.uname().machine
        if mach == 'Raspberry Pi Pico with rp2040':
            self.sp = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)
            cs = (board.GP5, board.GP6, board.GP7)
        elif mach.startswith("Adafruit Feather M4 Express"):
            self.sp = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
            cs = (board.D9, board.D6, board.D5)
        else:
            self.sp = busio.SPI(board.D13, MOSI=board.D11, MISO=board.D12)
            cs = (board.D8, board.D9, board.D10)
        def pin(p):
            r = digitalio.DigitalInOut(p)
            r.direction = digitalio.Direction.OUTPUT
            r.value = True
            return r
        self.cs = pin(cs[0])
        self.daz = pin(cs[2])
        self.setup_sd(cs[1])
        self.setup_spi()

    def setup_sd(self, sdcs):
        try:
            self.sdcard = sdcardio.SDCard(self.sp, sdcs)
        except OSError:
            return
        self.vfs = storage.VfsFat(self.sdcard)
        storage.mount(self.vfs, "/sd")

    @spilock
    def setup_spi(self):
        self.sp.configure(baudrate=15000000, phase=0, polarity=0)

    @spilock
    def dazzler(self, n):
        self.daz.value = False
        bb = bytearray(26)
        bb[0] = n
        self.sp.readinto(bb)
        self.daz.value = True
        return bb
        
    @spilock
    def controllers(self):
        self.daz.value = False
        bb = bytearray(26)
        self.sp.readinto(bb)
        self.daz.value = True
        return (self.wii_classic_pro(bb[2:8]), self.wii_classic_pro(bb[14:20]))
    
    @spilock
    def transfer(self, wr, rd = 0):
        self.cs.value = False
        self.sp.write(wr)
        r = None
        if rd != 0:
            r = bytearray(rd)
            self.sp.readinto(r)
        self.cs.value = True
        return r
