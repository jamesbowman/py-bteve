import array

from eveL import EVEL
from eveH import EVEH

class Dumper(EVEL, EVEH):
    def write(self, bb):
        for x in array.array('I', bb):
            print("%08x" % x)

import coverage
f = Dumper()
f.register(f)
coverage.cov0(f)
f.flush()
