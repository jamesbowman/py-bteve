import time
import sys

import bteve as EVE
from t_spidriver import SPI

if __name__ == '__main__':
    eve = EVE.ConnectedEVE(SPI(sys.argv[1]))
    helloworld(eve)
    eve.ClearColorRGB(0x20, 0x20, 0x20)
    eve.Clear()
    eve.flush()
    eve.cmd_text(20, 20, 31, 0, "Hello this is HDMI %dx%d" % (eve.w, eve.h))

    eve.PointSize(300)
    eve.Begin(EVE.POINTS)
    for i in range(8):
        x = 80 + 80 * i
        eve.ColorRGB(1 << i, 0, 0)
        eve.Vertex2f(x, 200)
        eve.ColorRGB(0, 1 << i, 0)
        eve.Vertex2f(x, 300)
        eve.ColorRGB(0, 0, 1 << i)
        eve.Vertex2f(x, 400)

    eve.cmd_memwrite(0, 2)
    eve.c(bytes([0x55, 0xaa, 0, 0]))

    eve.Begin(EVE.BITMAPS)
    eve.BlendFunc(EVE.SRC_ALPHA, 0)
    eve.cmd_setbitmap(0, EVE.L1, 2, 2)
    eve.BitmapSize(EVE.NEAREST, EVE.REPEAT, EVE.REPEAT, 64, 64)

    for i in range(0):
        x = 80 + 80 * i
        eve.ColorRGB(1 << i, 1 << i, 1 << i)
        eve.Vertex2f(x, 500)

    x0 = 13 * eve.w // 100
    x1 = 92 * eve.w // 100
    Y = eve.h // 11
    H = 50 * Y // 72
    y = 450
    for i,(cname, rgb) in enumerate([("red", 0xff0000), ("green", 0xff00), ("blue", 0xff), ("white", 0xffffff)]):
        # label(1 + i, cname)
        eve.SaveContext()
        eve.ScissorSize(x1 - x0, H)
        eve.ScissorXY(x0, y)
        eve.cmd_gradient(x0, 0, 0x000000, x1, 0, rgb)
        eve.RestoreContext()
        y += Y

    eve.swap()

    print('uptime', eve.rd32(EVE.REG_CLOCK) / 72e6)
    print('ID    ', hex(eve.rd32(EVE.REG_ID)))
    print('PCLK  ', eve.rd32(EVE.REG_PCLK))

    c0 = eve.rd32(EVE.REG_CLOCK)
    f0 = eve.rd32(EVE.REG_FRAMES)
    time.sleep(1)
    c1 = eve.rd32(EVE.REG_CLOCK)
    f1 = eve.rd32(EVE.REG_FRAMES)
    print('clocks', (c1 - c0), 'frames', f1 - f0)

