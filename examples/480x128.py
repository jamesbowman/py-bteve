import sys
import bteve as eve
import random

if sys.implementation.name == "circuitpython":
    gd = eve.Gameduino()
else:
    from spidriver import SPIDriver
    gd = eve.Gameduino(SPIDriver(sys.argv[1]))
gd.init()

def demo1(gd):
    gd.cmd_setrotate(0)
    gd.Clear()
    gd.Begin(eve.LINES)
    gd.ColorRGB(0, 128, 0)
    for y in range(0, 272, 16):
      gd.Vertex2f(0, y)
      gd.Vertex2f(480, y)
    gd.ColorRGB(255, 255, 255)
    for y in range(0, 272, 16):
      gd.cmd_text(0, y, 26, 0, "y=%d" % y)
    gd.swap()

def demo2(gd):
    if 0:
        gd.cmd_setrotate(0)
        gd.VertexTranslateY(144)
    gd.ClearColorRGB(0x00, 0x5f, 0x60)
    gd.Clear()
    gd.ColorRGB(0xff, 0xff, 0xff)
    gd.cmd_text(240, 32, 31, eve.OPT_CENTER, "Given that it's 2021, isn't")
    gd.cmd_text(240, 96, 31, eve.OPT_CENTER, "this much more suitable?")
    gd.swap()

def gray(i):
    gd.ColorRGB(i,i,i)

def demo3(gd):
    gd.Clear()
    gd.cmd_bgcolor(0x101010)

    for i in range(4):
        gray(0xb0)
        gd.cmd_gauge(60 + 120 * i, 64, 55, eve.OPT_FLAT, 4, 3, random.randrange(1000), 1000)
        gray(0xff)
        gd.cmd_text(60 + 120 * i, 104, 28, eve.OPT_CENTER, "ABCD"[i])
    gd.swap()

def demo4(gd):
    gd.ClearColorRGB(0xa3, 0xbe, 0x39)
    gd.Clear()

    SF = 4
    def btext(x, y, s):
        for c in s:
            gd.Vertex2ii(x, y, 16, ord(c))
            x += 8 * SF
    gd.cmd_scale(SF, SF)
    gd.cmd_setmatrix()
    gd.BitmapHandle(16)
    gd.BitmapSize(eve.NEAREST,eve.BORDER,eve.BORDER,8 * SF,16 * SF)
    gd.ColorRGB(0x1b, 0x28, 0x21)
    gd.Begin(eve.BITMAPS)
    btext(0, 64 - 10 * SF, '    LET YOUR')
    btext(0, 64 +  1 * SF, '  GEEK SHINE!')
    gd.RestoreContext()

    H = 90
    grid = bytes([
        H, H, H, H,
        H, 0, 0, 0,
        H, 0, 0, 0,
        H, 0, 0, 0,
        ])
    gd.ColorRGB(0xa3, 0xbe, 0x39)
    gd.cmd_memwrite(0, len(grid))
    gd.cc(grid)
    gd.BitmapHandle(0)
    gd.cmd_setbitmap(0, eve.L8, 4, 4)
    gd.BitmapSize(eve.NEAREST, eve.REPEAT, eve.REPEAT, gd.w, gd.h)
    gd.Vertex2f(0, 0)

    gd.swap()

def demo5(gd):
    gd.Clear()
    gd.swap()

    gd.cmd_loadimage(0, 0)
    gd.load(open("assets/sunflowers.jpg", "rb"))
    gd.Clear()
    gd.Begin(eve.BITMAPS)
    gd.Vertex2f(0, 0)
    gd.swap()

random.seed(0)
while 1:
    for d in [demo1, demo2, demo5, demo4, demo3]:
        gd.cmd_setrotate(1)
        d(gd)
        while True:
            gd.get_inputs()
            if gd.inputs.state.press:
                break
