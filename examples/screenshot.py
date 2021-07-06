import sys
import bteve as eve
import random

import minpng

if sys.implementation.name == "circuitpython":
    gd = eve.Gameduino()
else:
    from spidriver import SPIDriver
    gd = eve.Gameduino(SPIDriver(sys.argv[1]))
gd.init()

if 0:
    gd.ClearColorRGB(0x20, 0x40, 0x20)
    gd.Clear()
    gd.cmd_text(gd.w // 2, gd.h // 2, 31, eve.OPT_CENTER, "Hello world")
    gd.swap()
if 1:
    rr = random.randrange
    gd.VertexFormat(2)
    gd.Clear()
    gd.Begin(eve.POINTS)
    for i in range(100):
        gd.ColorRGB(rr(256), rr(256), rr(256))
        gd.PointSize(rr(gd.w // 6))
        gd.Vertex2f(rr(gd.w), rr(gd.h))
    gd.swap()

def screenshot(filename):
    with open(filename, "wb") as pngf:
        p = minpng.PngWriter(pngf.write, gd.w, gd.h)
        def handle_line(rgb):
            for i in range(gd.w):
                r = rgb[3 * i + 0]
                g = rgb[3 * i + 1]
                b = rgb[3 * i + 2]
                p.rgb(r, g, b)
        gd.screenshot(handle_line)

screenshot("/sd/foo.png")
