import array
print(array)
import bteve
print(array)

class Dumper(bteve.stem2):
    def write(self, bb):
        # print("---> WRITE called (%d)", len(bb), bb)
        for x in array.array('I', bb):
            print("%08x" % x)

f = Dumper()
f.register(f.write)
import coverage
coverage.cov0(f)

f.flush()
