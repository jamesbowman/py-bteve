"""Board-independent FT81x/BT81x register access, startup and command FIFO."""

import struct
import time

from .eve import BaseEVE
from .registers import (RAM_CMD, REG_CMD_READ, REG_CMDB_SPACE, REG_CMDB_WRITE,
                        REG_CPURESET, REG_FREQUENCY, REG_HSIZE, REG_ID, REG_VSIZE)

FIFO_MAX = 0xffc
# BRT_AN_033, section 2.3. The boot signature in RAM_G is valid after reset.
_CHIP_MODELS = {0x10: 810, 0x11: 811, 0x12: 812, 0x13: 813,
                0x15: 815, 0x16: 816, 0x17: 817, 0x18: 818}


class CoprocessorException(Exception):
    pass


class EVEDevice(BaseEVE):
    """Supply transfer(wr, rd=0) and a board with wake and configure_display hooks."""

    def init(self, minimal=False):
        self.register(self)
        self.coldstart()
        self._wait_register(REG_ID, "REG_ID", 0x7c)
        self._wait_register(REG_CPURESET, "REG_CPURESET", 0)

        signature = self.rd(0xc0000, 4)
        if len(signature) != 4 or signature[0] != 0x08 or signature[1] not in _CHIP_MODELS:
            raise ValueError("Unrecognized EVE chip signature: %r" % signature)
        self.chip_model = _CHIP_MODELS[signature[1]]
        expected = getattr(self.board, "model", None)
        if expected is not None and self.chip_model != expected:
            raise ValueError("Board expects EVE %d, detected %d" % (expected, self.chip_model))
        # Some CircuitPython native encoders have a fixed instruction set.
        if hasattr(self, "setmodel"):
            self.setmodel(self.chip_model)
        frequency = getattr(self.board, "system_frequency", None)
        if frequency is not None:
            self.wr32(REG_FREQUENCY, frequency)

        self.getspace()
        if minimal:
            self._read_dimensions()
        else:
            self.standard_startup()

    def _wait_register(self, address, name, expected):
        deadline = time.monotonic() + 1.0
        while True:
            value = self.rd8(address)
            if value == expected:
                return
            if time.monotonic() >= deadline:
                raise TimeoutError("EVE startup: %s stayed at 0x%02x (expected 0x%02x)"
                                   % (name, value, expected))
            time.sleep(0.005)

    def coldstart(self):
        self.board.wake(self)

    def standard_startup(self):
        self.board.configure_display(self)
        self._read_dimensions()

    def _read_dimensions(self):
        self.w = self.rd32(REG_HSIZE)
        self.h = self.rd32(REG_VSIZE)

    def host_cmd(self, a, b=0, c=0):
        self.transfer(bytes([a, b, c]))

    def _addr(self, a):
        return struct.pack(">I", a)[1:]

    def rd(self, a, n):
        return self.transfer(self._addr(a), 1 + n)[1:]

    def wr(self, a, v):
        self.transfer(self._addr(0x800000 | a) + v)

    def rd8(self, a):
        return self.rd(a, 1)[0]

    def rd16(self, a):
        return struct.unpack("<H", self.rd(a, 2))[0]

    def rd32(self, a):
        return struct.unpack("<I", self.rd(a, 4))[0]

    def wr8(self, a, v):
        self.wr(a, bytes([v]))

    def wr16(self, a, v):
        self.wr(a, struct.pack("<H", v))

    def wr32(self, a, v):
        self.wr(a, struct.pack("<I", v))

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

    def finish(self):
        self.flush()
        self.reserve(FIFO_MAX)

    def is_idle(self):
        return self.is_finished()

    def result(self, n=1):
        self.finish()
        wp = self.rd32(REG_CMD_READ)
        return self.rd32(RAM_CMD + (4095 & (wp - 4 * n)))
