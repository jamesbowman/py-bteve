import time
import struct

REG_ID = const(0x302000)
REG_HSIZE = const(0x302034)
REG_VSIZE = const(0x302048)
REG_CMDB_SPACE = const(0x302574)
REG_CMDB_WRITE = const(0x302578)
REG_GPIO = const(0x302094)
REG_PCLK = 0x302070

FIFO_MAX = const(0xffc)    # Maximum reported free space in the EVE command FIFO

class ConnectedEVE(stem2):
    def __init__(self, spi):
        self.spi = spi

        self.coldstart()

        t0 = time.time()
        while self.rd32(REG_ID) != 0x7c:
            assert (time.time() - t0) < 2.0, "No response - is device attached?"

        self.getspace()

    def coldstart(self):
        self.host_cmd(0x61, 0x46)   # 72 MHz
        self.host_cmd(0x48)         # int clock
        self.host_cmd(0x00)         # Wake up
        # self.host_cmd(0x68)       # Core reset

    def host_cmd(self, a, b = 0, c = 0):
        self.spi.transfer(bytes([a, b, c]))

    def standard_startup(self):
        self.Clear(1,1,1)
        self.swap()
        self.cmd_flashread(0, 0x1000, 0x1000)
        self.finish()
        print("%08x" % self.rd32(0xffc))
        if self.rd32(0xffc) == 0x7C6A0100:
            print('found flash config')
            self.c(self.rd(0, 512))
        self.finish()
        time.sleep(1)
        self.w = self.rd32(REG_HSIZE)
        self.h = self.rd32(REG_VSIZE)
        self.wr32(REG_GPIO, 0x83)
        print(self.w, self.h, self.rd32(REG_PCLK), hex(self.rd32(REG_GPIO)))

    def _addr(self, a):
        return struct.pack(">I", a)[1:]

    def rd(self, a, n):
        return self.spi.transfer(self._addr(a), 1 + n)[1:]

    def wr(self, a, v):
        self.spi.transfer(self._addr(0x800000 | a) + v)

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

    def result(self, n=1):
        # Return the result field of the preceding command
        self.finish()
        wp = self.rd32(REG_CMD_READ)
        return self.rd32(RAM_CMD + (4095 & (wp - 4 * n)))
