import sys
import time
import bteve as eve
import zlib
import struct
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

from spidriver import SPIDriver

def textmode(gd, mode = 'L'):
    font = ImageFont.truetype("../../.fonts/IBMPlexMono-SemiBold.otf", 13)
    ch = [chr(i) for i in range(32, 255)]

    im = Image.new("L", (256, 256))
    draw = ImageDraw.Draw(im)
    for c in ch:
        draw.text((128, 128), c, font=font, fill=255)
    (x0, y0, _, _) = im.getbbox()
    print(128 - x0, 128 - y0)
    im = im.crop(im.getbbox())
    # im.save("out.png")

    (w, h) = im.size

    fim = Image.new("L", (w, h * len(ch)))
    draw = ImageDraw.Draw(fim)
    for i,c in enumerate(ch):
        draw.text((128 - x0, (128 - y0) + (h * i)), c, font=font, fill=255)
    # fim.save("out.png")

    def size(a, b):
        gd.BitmapSize(eve.NEAREST, eve.BORDER, eve.BORDER, a, b)
        gd.BitmapSizeH(a >> 9, b >> 9)

    if mode == 'L':
        gd.cmd_setrotate(0)
        (sw, sh) = (1280, 720)
    elif mode == 'P':
        gd.cmd_setrotate(2)
        (sw, sh) = (720, 1280)

    w2 = w + 1
    h2 = h * 28 // 22
    (W, H) = (sw // w2, (sh // h2) + 1)
    ht = H * h2
    y_bar = (sh - (H - 1) * h2) // 2
    x_bar = (sw - (W * w2)) // 2

    gx = w * ht             # glyph x term
    gy = w * h2             # glyph y term
    cx = 2 * H              # color x term
    cz = 2 * H * W          # color z term
    wh = w * h
    sz = w * W * h2 * H

    cm = 0
    fm = cm + 2 * cz
    fb = fm + len(fim.tobytes())

    gd.Clear()
    gd.swap()

    gd.cmd_inflate(fm)
    c = eve.align4(zlib.compress(fim.tobytes()))
    gd.cc(c)

    print('font size', (w, h), (w2, h2), 'screen size', (W, H - 1))
    print('font bytes', len(fim.tobytes()))
    print('bars:', (x_bar, y_bar))

    gd.BitmapHandle(0)
    gd.cmd_setbitmap(fb, eve.L8, w, ht)
    gd.cmd_memset(fb, 0x00, W * w * ht)

    gd.BitmapHandle(1)
    gd.cmd_setbitmap(cm, eve.RGB565, 1, H)
    size(w2, ht)
    if 0:
        b = bytes([rr(256) for i in range(2 * 2 * W * H)])
        gd.cmd_memwrite(cm, len(b))
        gd.cc(eve.align4(b))
    else:
        gd.cmd_memzero(cm, 2 * 2 * W * H)

    #  : moded create does> mode @ cells + @ ;
    with open("_textmode.fs", "wt") as f:
        for v in ("fm", "fb", "cm", "sz"):
            f.write("$%x. 2constant %s\n" % (eval(v), v))
        for v in ("H", "W", "gx", "gy", "cx", "cz", "wh", "y_bar", "h2"):
            f.write("$%x constant %s\n" % (eval(v), v))

    def gaddr(x, y):
        return fb + w * ((y * h2) + (x * ht))
    def caddr(x, y, z):
        return cm + 2 * (y + H * (x + z * W))
    def drawch(x, y, c, color = 0xffff, bg = 0x0000):
        dst = gaddr(x, y)
        src = fm + (ord(c) - 0x20) * (w * h)
        gd.cmd_memcpy(dst, src, (w * h))
        # gd.cmd_memset(dst, 0xff, (w * h))

        gd.cmd_memwrite(caddr(x, y, 0), 2)
        gd.cc(struct.pack("<I", color))
        gd.cmd_memwrite(caddr(x, y, 1), 2)
        gd.cc(struct.pack("<I", bg))

    offset = 0
    vh = y_bar + ((H - offset) * h2)

    def drawtwice(x):
        gd.Macro(0)
        if x:
            yo = 0
        else:
            yo = (h2 - h) // 2
        for i in range(sw // w2):
            gd.Cell(i)
            gd.Vertex2f(x_bar + x + w2 * i, -ht + yo)
            gd.Vertex2f(x_bar + x + w2 * i, 0 + yo)

    def color_panel(z):
        gd.SaveContext()
        gd.BitmapHandle(1)
        gd.BitmapSource(caddr(0, 0, z))
        gd.BitmapTransformA(0, 1)
        gd.BitmapTransformE(32768 // h2 + 1, 1)
        drawtwice(-1)
        gd.RestoreContext()

    gd.cmd_memwrite(eve.REG_MACRO_0, 4)
    gd.VertexTranslateY(vh << 4)

    gd.VertexFormat(0)
    gd.ClearColorA(0)
    # gd.ClearColorRGB(200, 200, 200)
    gd.Clear()
    gd.ScissorXY(x_bar, y_bar)
    gd.ScissorSize((W * w2), (H - 1) * h2)
    gd.Begin(eve.BITMAPS)

    gd.ColorMask(1, 1, 1, 0)
    color_panel(1)

    gd.ColorMask(0, 0, 0, 1)
    gd.BlendFunc(1, 0)
    gd.BitmapHandle(0)
    drawtwice(0)

    gd.ColorMask(1, 1, 1, 0)
    gd.BlendFunc(eve.DST_ALPHA, eve.ONE_MINUS_DST_ALPHA)
    color_panel(0)

    gd.swap()

    if 0:
        for i in range(H):
            s = "[{0}]".format(i)
            for j,c in enumerate(s):
                drawch(i + j, i, c, 0xffff, 0x1010)
    if 1:
        for i in range(W):
            for j in range(H-1):
                edge = (i in [0,W-1]) or (j in [0,H-2])
                drawch(i, j, '.x'[edge], 0xffff, 0x1010)
    gd.finish()

if __name__ == "__main__":
    gd = eve.GameduinoSPIDriver(SPIDriver(sys.argv[1]))
    gd.init()
    textmode(gd)

