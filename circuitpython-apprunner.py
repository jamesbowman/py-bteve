import os
from bteve import Gameduino

import time
import struct

import board
import busio
import digitalio

import sdcardio
import storage

# from rpsoftspi import SPI
# from rppiospi import SPI
from busio import SPI

def spilock(f):
    def wrapper(*args):
        spi = args[0].sp
        while not spi.try_lock():
            pass
        r = f(*args)
        spi.unlock()
        return r
    return wrapper

def spilock1(f):
    def wrapper(*args):
        spi = args[0].sp1
        while not spi.try_lock():
            pass
        r = f(*args)
        spi.unlock()
        return r
    return wrapper


def pin(p):
    r = digitalio.DigitalInOut(p)
    r.direction = digitalio.Direction.OUTPUT
    r.value = True
    return r

def reset(p):
    pgm = pin(p)
    pgm.value = False
    time.sleep(.1)
    pgm.value = True
    time.sleep(.6)
    return pgm

class MM2040EV(Gameduino):
    def __init__(self):
        mach = os.uname().machine
        print('mach', mach)
        if mach == 'Raspberry Pi Pico with rp2040':
            self.sp = busio.SPI(board.GP2, MOSI=board.GP3, MISO=board.GP4)
            cs = (board.GP5, board.GP6, board.GP7)
            # self.rp = reset(board.GP7)
        elif mach.startswith("Adafruit Feather M4 Express"):
            self.sp = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
            cs = (board.D4, board.D5, board.D6)
            self.rp = reset(board.D9)
        elif mach.startswith("Teensy 4."):
            self.sp = busio.SPI(board.D13, MOSI=board.D11, MISO=board.D12)
            cs = (board.D8, board.D9, board.D10)
            self.rp = reset(board.D16)
        else:
            # Adafruit Metro M4 Express
            # follows the Arduino pin numbering
            self.sp = busio.SPI(board.D13, MOSI=board.D11, MISO=board.D12)
            cs = (board.D8, board.D9, board.D10)

        self.cs = pin(cs[0])
        # self.sp1 = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
        # print(self.setup_sd())
        self.setup_spi()

    @spilock1
    def setup_spi1(self):
        self.sp1.configure(baudrate=1000000, phase=0, polarity=0)

    def setup_sd(self):
        try:
            print(f"sdcardio.SDCard({self.sp1}, {board.GP13})")
            self.sdcard = sdcardio.SDCard(self.sp1, board.GP13)
        except OSError:
            return False
        self.vfs = storage.VfsFat(self.sdcard)
        storage.mount(self.vfs, "/sd")
        return True

def run(app):
    gd = MM2040EV()
    gd.init()
    app(gd)
    gd.cmd_memset(0, 65, 4)
    gd.finish()
    print(hex(gd.rd32(0)))
