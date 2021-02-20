import sys
import random
import bteve as eve

rr = random.randrange

if sys.implementation.name == "circuitpython":
    gd = eve.Gameduino()
else:
    from spidriver import SPIDriver
    gd = eve.Gameduino(SPIDriver(sys.argv[1]))
gd.init()

gd.Clear()
s_sketch = gd.w * gd.h // 8
gd.cmd_memzero(0, s_sketch)
gd.cmd_sketch(0, 0, gd.w, gd.h, 0, eve.L1)

gd.cmd_setbitmap(0, eve.L1, gd.w, gd.h)
gd.Begin(eve.BITMAPS)
gd.Vertex2f(0, 0)
gd.swap()
