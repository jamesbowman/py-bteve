import time
from collections import namedtuple

from .device import CoprocessorException, EVEDevice, FIFO_MAX
from .registers import *

"""
Adapted from https://github.com/jfurcean/CircuitPython_WiiChuck.git
where this class ClassicController appears. It is covered by this license

The MIT License (MIT)
  
Copyright (c) 2021 John Furcean

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class ClassicController:
    """
    Class which provides interface to Nintendo Wii Classic Controller.

    :param b6: 6 byte raw wii controller readout
    """

    _Values = namedtuple("Values", ("joysticks", "buttons", "dpad", "triggers"))
    _Joysticks = namedtuple("Joysticks", ("rx", "ry", "lx", "ly"))
    _Buttons = namedtuple(
        "Buttons",
        (
            "A",
            "B",
            "X",
            "Y",
            "R",
            "L",
            "ZR",
            "ZL",
            "start",
            "select",
            "home",
            "plus",
            "minus",
        ),
    )
    _Dpad = namedtuple("Dpad", ("up", "down", "right", "left"))
    _Triggers = namedtuple("Trigers", ("right", "left"))

    def __init__(self, b6):
        assert len(b6) == 6
        if b6 == b'\x00\x00\x00\x00\x00\x00':
            self.buffer = b'\xff\xff\xff\xff\xff\xff'
        else:
            self.buffer = b6

    @property
    def values(self):
        """The current state of all values."""
        return self._Values(
            self._joysticks(),
            self._buttons(),
            self._dpad(),
            self._triggers(),
        )

    @property
    def joysticks(self):
        """The current joysticks positions."""
        return self._joysticks()

    @property
    def buttons(self):
        """The current pressed state of all buttons."""
        return self._buttons()

    @property
    def dpad(self):
        """The current pressed state of the dpad."""
        return self._dpad()

    @property
    def triggers(self):
        """The current readding from the triggers (0-31 for Pro) (0 or 31 non-Pro)."""
        return self._triggers()

    def _joysticks(self):
        return self._Joysticks(
            (
                (self.buffer[0] & 0xC0) >> 3
                | (self.buffer[1] & 0xC0) >> 5
                | (self.buffer[2] & 0x80) >> 7
            ),  # rx
            self.buffer[2] & 0x1F,  # ry
            self.buffer[0] & 0x3F,  # lx
            self.buffer[1] & 0x3F,  # ly
        )

    def _buttons(self):
        return self._Buttons(
            not bool(self.buffer[5] & 0x10),  # A
            not bool(self.buffer[5] & 0x40),  # B
            not bool(self.buffer[5] & 0x8),  # X
            not bool(self.buffer[5] & 0x20),  # Y
            not bool(self.buffer[4] & 0x2),  # R
            not bool(self.buffer[4] & 0x20),  # L
            not bool(self.buffer[5] & 0x4),  # ZR
            not bool(self.buffer[5] & 0x80),  # ZL
            not bool(self.buffer[4] & 0x4),  # start
            not bool(self.buffer[4] & 0x10),  # select
            not bool(self.buffer[4] & 0x8),  # home
            not bool(self.buffer[4] & 0x4),  # plus
            not bool(self.buffer[4] & 0x10),  # minus
        )

    def _dpad(self):
        return self._Dpad(
            not bool(self.buffer[5] & 0x1),  # UP
            not bool(self.buffer[4] & 0x40),  # DOWN
            not bool(self.buffer[4] & 0x80),  # RIGHT
            not bool(self.buffer[5] & 0x2),  # LEFT
        )

    def _triggers(self):
        return self._Triggers(
            self.buffer[3] & 0x1F,  # right
            (self.buffer[2] & 0x60) >> 2 | (self.buffer[3] & 0xE0) >> 5,  # left
        )


class GameduinoProfile:
    def wake(self, device):
        device.host_cmd(0x00)  # ACTIVE
        device.host_cmd(0x68)  # Core reset

    def configure_display(self, device):
        device.Clear(1, 1, 1)
        device.swap()
        device.cmd_flashread(0, 0x1000, 0x1000)
        device.finish()
        time.sleep(.1)
        if device.rd32(0xffc) == 0x7C6A0100:
            device.cc(device.rd(0, 512))
        else:
            print('*** Did not find flash config ***')
        device.finish()
        device.cmd_regwrite(REG_GPIO, 0x83)
        time.sleep(.1)


class Gameduino(EVEDevice):
    board = GameduinoProfile()

    def bringup(self):
        """Continuously print raw REG_ID transactions for SPI troubleshooting."""
        time.sleep(.4)
        while True:
            self.d.sel()
            try:
                for c in (0x30, 0x20, 0x00, 0xff, 0xff, 0xff):
                    r = self.d.writeread(bytes([c]))[0]
                    print("Sent %02x recv %02x" % (c, r))
            finally:
                self.d.unsel()
            time.sleep(2)

    def wii_classic_pro(self, b):
        return ClassicController(b)
