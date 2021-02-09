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

while True:
    gd.Clear()
    gd.Begin(eve.POINTS)
    for i in range(100):
        gd.ColorRGB(rr(256), rr(256), rr(256))
        gd.PointSize(rr(100))
        gd.Vertex2f(rr(gd.w), rr(gd.h))
    gd.swap()
