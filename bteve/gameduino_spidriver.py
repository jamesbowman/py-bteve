import struct

from .device import EVEDevice
from .gameduino import Gameduino


class SPIDriverTransport:
    """EVE SPI transactions using the adapter's primary chip select."""

    def __init__(self, driver):
        self.d = driver
        driver.unsel()

    def transfer(self, wr, rd=0):
        self.d.sel()
        try:
            self.d.write(wr)
            return self.d.read(rd)
        finally:
            self.d.unsel()

    def close(self):
        try:
            self.d.unsel()
        finally:
            self.d.close()


class SPIDriverDevice(SPIDriverTransport, EVEDevice):
    def __init__(self, driver, board):
        super().__init__(driver)
        self.board = board


class GameduinoSPIDriver(SPIDriverTransport, Gameduino):
    def __init__(self, d):
        super().__init__(d)
        self.d.seta(1)
        self.d.setb(1)

    def dazzler_cmd(self, a, b=0):
        self.d.setb(0)
        try:
            return struct.unpack("BB", self.d.writeread(struct.pack("BB", a, b)))
        finally:
            self.d.setb(1)

    def controllers(self):
        self.d.setb(0)
        try:
            bb = self.d.writeread(b'\x00' * 26)
        finally:
            self.d.setb(1)
        return (self.wii_classic_pro(bb[2:8]), self.wii_classic_pro(bb[14:20]))
