import array
from binascii import crc32

import coverage
from bteve import Gameduino

class Dumper(Gameduino):
    def __init__(self):
        self.d = []
    def write(self, bb):
        self.d.append(bb)

f = Dumper()
f.register(f)
coverage.cov0(f)
f.flush()
actual = crc32(b"".join(f.d))
expected = 0x86d4ce43
print('actual', hex(actual), 'expected', hex(expected))
assert actual == expected
