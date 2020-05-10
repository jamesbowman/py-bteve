import sys
import time
import gameduino as GD
import math
import struct
import random

def info(eve):
    settings = [
        (GD.REG_OUTBITS, 0),
        (GD.REG_DITHER, 0),
        (GD.REG_ROTATE, 0),
        (GD.REG_SWIZZLE, 0),
        (GD.REG_HCYCLE, 1650),
        (GD.REG_HSYNC1, 110),
        (GD.REG_HSYNC0, 110 + 40),
        (GD.REG_HOFFSET, 1650 - 1280 - 1),
        (GD.REG_HSIZE, 1280),
        (GD.REG_VCYCLE, 750),
        (GD.REG_VOFFSET, 750 - 720 - 1),
        (GD.REG_VSIZE, 720),
        (GD.REG_CSPREAD, 0),
        (GD.REG_PCLK_POL, 0),

        (GD.REG_GPIO, 0x83),

        (GD.REG_PCLK, 1)
    ]
    # for (r,v) in settings: eve.cmd_regwrite(r, v)
    eve.finish()
    c0 = eve.rd32(GD.REG_CLOCK)
    f0 = eve.rd32(GD.REG_FRAMES)
    time.sleep(1)
    c1 = eve.rd32(GD.REG_CLOCK)
    f1 = eve.rd32(GD.REG_FRAMES)
    print("main clock %.1f MHz, %d fps" % ((c1 - c0) * 1e-6, (f1 - f0)))
    for nm in "HSIZE HOFFSET HSYNC0 HSYNC1 HCYCLE VSIZE VOFFSET VSYNC0 VSYNC1 VCYCLE FLASH_STATUS".split():
        v = eve.rd32(eval("GD.REG_" + nm))
        print("REG_%-12s %d %#x" % (nm, v, v))

def blinka(eve):
    eve.BitmapHandle(0)
    eve.cmd_loadimage(0, GD.OPT_FULLSCREEN)
    scale_factor = eve.w / 480
    eve.load(open("circuitpython.png", "rb"))

    eve.BitmapHandle(1)
    eve.cmd_loadimage(-1, 0)
    eve.load(open("blinka100.png", "rb"))
    eve.BitmapSize(GD.BILINEAR, GD.BORDER, GD.BORDER, 100, 100)

    r = 100                                 # radius for circle of Blinkas

    (cx, cy) = (eve.w / 2, eve.h / 2)

    for t in range(0, 3600, 2):
        eve.Clear(1,1,1)
        eve.Begin(GD.BITMAPS)
        eve.BitmapHandle(0)                 # Draw the background
        eve.cmd_scale(scale_factor, scale_factor)
        eve.cmd_setmatrix()
        eve.Vertex2f(0, 0)
        eve.RestoreContext()
        eve.cmd_text(4, 4, 31, 0, "CircuitPython at %d x %d" % (eve.w, eve.h))

        eve.BitmapHandle(1)                 # Ten Blinkas, 36 degrees apart
        N = 10
        for i in range(N):
            angle = 360 * i / N + t
            eve.cmd_loadidentity()
            eve.cmd_rotatearound(50, 50, angle)
            eve.cmd_setmatrix()
            th = math.radians(-angle)
            x = r * math.sin(th)
            y = r * math.cos(th)
            eve.Vertex2f(cx - 50 + x, cy - 50 + y)
        eve.swap()

def fizz(eve):
    rr = random.randrange
    while True:
        eve.Clear(1, 1, 1)
        eve.Begin(GD.POINTS)
        # random.seed(7)
        # eve.finish()

        t0 = eve.rd32(GD.REG_CLOCK)
        for i in range(100):
            eve.ColorRGB(rr(256), rr(256), rr(256))
            eve.PointSize(100 + rr(900))
            eve.Vertex2f(rr(eve.w), rr(eve.h))

        t1 = eve.rd32(GD.REG_CLOCK)
        print('took', 1000 * (0xffffffff & (t1 - t0)) / 60e6, 'ms')
        eve.swap()

def asteroid(eve):
    import ren_ast
    r = ren_ast.Renderer(eve)
    while True:
        r.draw()
        eve.swap()
        # eve.screenshot_im().save("out.png") ; break

def hqtext(eve):
    import textwrap

    eve.cmd_loadimage(0, 0)
    eve.load(open("monospace/fim.png", "rb"))
    (w, h, h2) = (11, 19, 23)

    eve.BitmapHandle(0)
    fb = 0x10000
    eve.cmd_setbitmap(fb, GD.L8, 11, 720)
    eve.cmd_memset(fb, 0x00, 1280 * 720)

    eve.BitmapHandle(1)
    cm = 0x8000
    eve.cmd_setbitmap(cm, GD.RGB565, 116, 31)
    eve.BitmapSize(GD.NEAREST, GD.BORDER, GD.BORDER, 0, 0)
    random.seed(7)
    b = bytes([random.randrange(256) for i in range(2 * 116 * 31)])
    eve.cmd_memwrite(cm, len(b))
    eve.cc(b)

    def drawch(x, y, c, color = 0x1234):
        eve.cmd_memcpy(fb + y * (w * h2) + (x * w * 720),
                       (ord(c) - 0x20) * (w * h),
                       (w * h))
        eve.cmd_memwrite(cm + 2 * (x + 116 * y), 2)
        eve.cc(struct.pack("<I", color))

    paras = open("monospace/moby2").read().split("\n")
    txt = "\n".join([textwrap.fill(p, 1280 // w) for p in paras])
    (x, y) = (0, 0)
    color = random.randrange(0x10000)
    for c in txt:
        if c == ' ':
            color = random.randrange(0x10000)
        if c == '\n':
            x = 0
            y += 1
        else:
            drawch(x, y, c, color)
            x += 1
        if y > (720 // h2):
            break
    if 1:
        eve.VertexFormat(3)
        eve.Clear()
        eve.Begin(GD.BITMAPS)
        eve.BlendFunc(1, 0)
        eve.BitmapHandle(0)
        for i in range(1280 // 11):
            eve.Cell(i)
            eve.Vertex2f(11 * i, 0)

        eve.BitmapHandle(1)
        eve.Cell(0)
        eve.cmd_scale(w, h2)
        eve.cmd_setmatrix()
        eve.BlendFunc(GD.DST_ALPHA, 0)
        eve.Vertex2f(0, 0)

        eve.swap()
        eve.finish()
    
if sys.implementation.name == "circuitpython":
    from gameduino_circuitpython import GameduinoCircuitPython
    eve = GameduinoCircuitPython()
else:
    from gameduino_spidriver import GameduinoSPIDriver
    eve = GameduinoSPIDriver()
eve.init()
info(eve)
asteroid(eve)
# hqtext(eve)
