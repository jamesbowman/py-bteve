import sys
import os
import zlib
import time

from gameduino_spidriver import GameduinoSPIDriver
from eve import EVE, align4
import registers as gd3
from PIL import Image, ImageFont, ImageDraw, ImageChops
import gameduino2.prep
from gameduino2.convert import convert

class LoggingGameduinoSPIDriver(GameduinoSPIDriver):
    
    def __init__(self):
        GameduinoSPIDriver.__init__(self)

        self.seq = 0
        self.spool()

    def spool(self):
        self.cmd_dump = open("%04d.cmd" % self.seq, "wb")
        self.seq += 1

    def write(self, s):
        GameduinoSPIDriver.write(self, s)
        self.cmd_dump.write(s)

    def swap(self):
        GameduinoSPIDriver.swap(self)
        self.spool()

def gentext(s, h):
    fn = "../../.fonts/IBMPlexSans-SemiBold.otf"
    fn = "../../.fonts/Arista-Pro-Alternate-Light-trial.ttf"
    font = ImageFont.truetype(fn, h)
    im = Image.new("L", (8000, 1000))
    draw = ImageDraw.Draw(im)
    draw.text((1, 1), s, font=font, fill = 255)
    return im.crop(im.getbbox())

    glow = im.filter(ImageFilter.GaussianBlur(10))
    im = ImageChops.add(im, glow)
    return im.crop(im.getbbox())

def mkbanner():
    im = gentext("dazzler", 1100)
    blank = Image.new("L", im.size, 0)
    # im.transpose(Image.FLIP_TOP_BOTTOM).save("dazzler.png")
    hard = im.point(lambda x: [0,255][x != 0])
    a = hard.load()
    pos = []
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if a[x,y] == 255:
                ImageDraw.floodfill(hard, (x, y), 128)
                hard.save("out.png")
                matte = hard.point(lambda x: [0,255][x == 128])
                ImageDraw.floodfill(hard, (x, y), 0)
                s = ImageChops.composite(im, blank, matte)
                (x0, y0, x1, y1) = s.getbbox()

                s = s.crop((x0, y0, x1, y1))
                pos.append((x0, y0) + s.size + (s, ))
    pos = sorted(pos)

    for i,pp in enumerate(pos):
        (x, y, w, h, s) = pp
        s.transpose(Image.FLIP_TOP_BOTTOM).save("tmp.png")
        os.system("astcenc -c tmp.png %d.astc 10x8 -thorough" % i)
    return [(x, y, w, h) for (x, y, w, h, s) in pos]

if __name__ == "__main__":
    if 0:
        print(mkbanner())
        sys.exit(0)
    banner_pos = [(0, 0, 525, 713), (599, 188, 520, 525), (1192, 189, 498, 518), (1737, 189, 498, 518), (2321, 3, 212, 705), (2567, 189, 527, 525), (3164, 189, 314, 518)]

    gd = LoggingGameduinoSPIDriver()
    gd.init()
    gd.cmd_flashfast()

    from dogfight import Dogfight
    from instruments import Instruments

    a = 0
    locs = []
    for i in range(7):
        gd.BitmapHandle(i)
        (bw, bh, d) = gameduino2.prep.astc_tile(open("%d.astc" % i, "rb"))
        gd.cmd_inflate(a)
        gd.cc(align4(zlib.compress(d)))
        locs.append(a)
        a += len(d)
    print('used', a)
    dg = Dogfight({'ships' : 8192}, a)
    ins = Instruments({}, a)

    # time.sleep(4)
    for xo in range(-800, 2600, 4):
    # for xo in range(300, 1000, 4):
        print(xo)
        gd.VertexFormat(2)
        gd.Clear()
        gd.VertexTranslateX(16 * -xo)

        ins.run(gd)

        gd.SaveContext()
        gd.Begin(gd3.BITMAPS)
        gd.ColorA(0x80)
        for i in range(7):
            (x, y, w, h) = banner_pos[i]
            gd.BitmapHandle(i)
            gd.cmd_setbitmap(locs[i], gd3.ASTC_10x8, w, h)
            gd.BitmapSwizzle(1, 1, 1, gd3.RED)
            gd.Vertex2f(x, y)
        gd.RestoreContext()

        gd.BitmapHandle(14)
        if 1 and xo < 1200:
            dg.run(gd)

        gd.swap()
        gd.finish()
