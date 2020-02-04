import array

from eveL import EVEL

class Dumper(EVEL):
    def write(self, b):
        f.bb += b

f = Dumper()
f.register(f)
f.bb = b''
f.ClearColorRGB(0x12, 0x34, 0x56)
f.flush()
assert list(array.array("I", f.bb)) == [0x02123456], "Unexpected output %r" % f.bb
print("eveL smoke test passed")

