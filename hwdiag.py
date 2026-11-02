"""Check EVE communication without requiring a display configuration."""

import bteve as eve
import apprunner
from binascii import crc32


def main(gd):
    print("REG_ID: 0x{:02x}".format(gd.rd32(eve.REG_ID)))
    print("Display: {} x {}".format(gd.w, gd.h))
    print("Command FIFO free: {} bytes".format(gd.rd32(eve.REG_CMDB_SPACE)))
    # A result-bearing command verifies both FIFO writes and memory reads.
    expected = crc32(gd.rd(0, 4)) & 0xffffffff
    gd.cmd_memcrc(0, 4, 0)
    actual = gd.result()
    if actual != expected:
        raise RuntimeError("RAM_G CRC mismatch: {:08x} != {:08x}".format(actual, expected))
    print("RAM_G[0:4] CRC: 0x{:08x} (verified)".format(actual))


if __name__ == "__main__":
    apprunner.run(main, minimal=True)
