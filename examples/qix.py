import sys
import time
import math
import random
import bteve as eve

if sys.implementation.name == "circuitpython":
    gd = eve.Gameduino()
else:
    from spidriver import SPIDriver
    gd = eve.Gameduino(SPIDriver(sys.argv[1]))
gd.init()

def tri(t):
    return 2 * abs(math.fmod(t, 1.0) - 0.5)

def at(t, ff):
    x = gd.w * tri(ff[0] * t)
    y = gd.h * tri(ff[1] * t) - 10
    gd.Vertex2f(x, y)

random.seed(0)
F = [random.random() for i in range(9)]

while True:
    t = time.monotonic_ns() / 18000000
    gd.Clear()
    gd.VertexFormat(3)
    gd.LineWidth(3)
    for dt in range(0, 30, 3):
        gd.Begin(eve.LINE_STRIP)
        tn = (t - dt) / 150
        gd.ColorRGB(
            int(255 * tri(F[6] * tn)),
            int(255 * tri(F[7] * tn)),
            int(255 * tri(F[8] * tn)))
        at(tn, F[0:2])
        at(tn, F[2:4])
        at(tn, F[4:6])
        at(tn, F[0:2])

    gd.swap()
