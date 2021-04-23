import sys
import time
import struct
from collections import namedtuple

if sys.implementation.name == 'circuitpython':
    from _eve import _EVE
else:
    from ._eve import _EVE
from .eve import EVE
from .registers import *

if sys.implementation.name != "circuitpython":
    def const(x): return x

REG_ID = const(0x302000)
REG_HSIZE = const(0x302034)
REG_VSIZE = const(0x302048)
REG_CMDB_SPACE = const(0x302574)
REG_CMDB_WRITE = const(0x302578)
REG_GPIO = const(0x302094)
REG_PCLK = 0x302070
REG_PWM_DUTY = 0x3020d4
REG_PWM_HZ = 0x3020d0

FIFO_MAX = const(0xffc)    # Maximum reported free space in the EVE command FIFO

class CoprocessorException(Exception):
    pass

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

class Gameduino(_EVE, EVE):
    def init(self):
        self.register(self)

        self.coldstart()

        # self.bringup()

        t0 = time.monotonic()
        while self.rd32(REG_ID) != 0x7c:
            assert (time.monotonic() - t0) < 1.0, "No response - is device attached?"

        self.getspace()

        # print("ID %x  %x %x %x %x" % (
        #     self.rd32(REG_ID),
        #     self.rd32(0xc0000),
        #     self.rd32(REG_HSIZE),
        #     self.rd32(REG_VSIZE),
        #     self.rd32(REG_CMDB_SPACE)))

        self.standard_startup()

    def coldstart(self):
        # self.host_cmd(0x61, 0x46)   # 72 MHz
        # self.host_cmd(0x44)         # int clock
        self.host_cmd(0x00)         # Wake up
        self.host_cmd(0x68)         # Core reset

    def bringup(self):
        time.sleep(.4)

        while 1:
            print()
            self.d.sel()
            for c in (0x30, 0x20, 0x00, 0xff, 0xff, 0xff):
                r = self.d.writeread(bytes([c]))[0]
                print("Sent %02x recv %02x" % (c, r))
            self.d.unsel()
            time.sleep(2)

    def host_cmd(self, a, b = 0, c = 0):
        self.transfer(bytes([a, b, c]))

    def standard_startup(self):
        self.Clear(1,1,1)
        self.swap()
        self.cmd_flashread(0, 0x1000, 0x1000)
        self.finish()
        # print('*** Done flash ***')
        time.sleep(.1)
        if self.rd32(0xffc) == 0x7C6A0100:
            self.cc(self.rd(0, 512))
        else:
            print('*** Did not find flash config ***')
        self.finish()
        self.w = self.rd32(REG_HSIZE)
        self.h = self.rd32(REG_VSIZE)
        # self.wr32(REG_GPIO, 0x83)
        # print(self.w, self.h, self.rd32(REG_PCLK), hex(self.rd32(REG_GPIO)))
        self.cmd_regwrite(REG_GPIO, 0x83)
        time.sleep(.1)

    def _addr(self, a):
        return struct.pack(">I", a)[1:]

    def rd(self, a, n):
        return self.transfer(self._addr(a), 1 + n)[1:]

    def wr(self, a, v):
        self.transfer(self._addr(0x800000 | a) + v)

    def rd32(self, a):
        return struct.unpack("<I", self.rd(a, 4))[0]

    def wr32(self, a, v):
        self.wr(a, struct.pack("I", v))

    def getspace(self):
        self.space = self.rd32(REG_CMDB_SPACE)
        if self.space & 1:
            raise CoprocessorException

    def reserve(self, n):
        while self.space < n:
            self.getspace()

    def is_finished(self):
        self.getspace()
        return self.space == FIFO_MAX
            
    def write(self, ss):
        self.reserve(len(ss))
        self.wr(REG_CMDB_WRITE, ss)
        self.space -= len(ss)
        return


        # Write ss to the command FIFO
        for i in range(0, len(ss), 64):
            s = ss[i:i + 64]
            self.reserve(len(s))
            self.wr(REG_CMDB_WRITE, s)
            self.space -= len(s)

    def finish(self):
        self.flush()
        self.reserve(FIFO_MAX)

    def is_idle(self):
        self.getspace()
        return self.space == FIFO_MAX

    def wii_classic_pro(self, b):
        return ClassicController(b)

    def result(self, n=1):
        # Return the result field of the preceding command
        self.finish()
        wp = self.rd32(REG_CMD_READ)
        return self.rd32(RAM_CMD + (4095 & (wp - 4 * n)))
