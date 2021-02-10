import sys
import time
import struct
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

WII_none = {'bh': 0, 'brt': 0, 'b-': 0, '.': 0, 'b+': 0, 'bdd': 0, 'blt': 0, 'ly': 32, 'lx': 32, 'rx': 16, 'bdl': 0, 'rt': 0, 'bdr': 0, 'bb': 0, 'ba': 0, 'by': 0, 'bx': 0, 'bzl': 0, 'bdu': 0, 'bzr': 0, 'lt': 0, 'ry': 16}

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
        if (b[4] & 1 == 0) or (b == bytes([160, 32, 16, 0, 255, 255])):
            return WII_none
        b4 = ~b[4]
        b5 = ~b[5]
        return {
            'brt' : 1 & (b4 >> 1),
            'b+'  : 1 & (b4 >> 2),
            'bh'  : 1 & (b4 >> 3),
            'b-'  : 1 & (b4 >> 4),
            'blt' : 1 & (b4 >> 5),
            'bdd' : 1 & (b4 >> 6),
            'bdr' : 1 & (b4 >> 7),

            'bdu' : 1 & (b5 >> 0),
            'bdl' : 1 & (b5 >> 1),
            'bzr' : 1 & (b5 >> 2),
            'bx'  : 1 & (b5 >> 3),
            'ba'  : 1 & (b5 >> 4),
            'by'  : 1 & (b5 >> 5),
            'bb'  : 1 & (b5 >> 6),
            'bzl' : 1 & (b5 >> 7),

            'lx' : b[0] & 63,
            'ly' : b[1] & 63,
            'rx' : (((b[0] >> 6) & 3) << 3) |
                   (((b[1] >> 6) & 3) << 1) |
                   (((b[2] >> 7) & 1)),
            'ry' : b[2] & 31,
            'lt' : (((b[2] >> 5) & 3) << 3) |
                   (((b[3] >> 5) & 7)),
            'rt' : b[3] & 31,
        }

    def result(self, n=1):
        # Return the result field of the preceding command
        self.finish()
        wp = self.rd32(REG_CMD_READ)
        return self.rd32(RAM_CMD + (4095 & (wp - 4 * n)))
