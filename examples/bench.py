import time
from sweveL import EVEL
from eveH import EVEH

class Sink(EVEL, EVEH):
    def write(self, bb):
        pass

eve = Sink()
eve.register(eve)

def T():
    # return time.ticks_us() / 1e6
    return time.monotonic()

eve.flush()
t0 = T()
for i in range(1000):
    eve.Vertex2f(i, i)
    # eve.cmd_append(0x120, 0)
eve.flush()
t1 = T()
print(t1 - t0)
msg = "1000 points took %.1f ms" % ((t1 - t0) * 1000)
print(msg)
