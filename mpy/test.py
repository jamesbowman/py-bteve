import sys
import bteve

class Dumper(bteve.stem):
    def write(self, bb):
        print("---> WRITE called", bb)

f = Dumper()
f.register(f.write)
f.PointSize(0x5a)

print('flush:', f.flush())
