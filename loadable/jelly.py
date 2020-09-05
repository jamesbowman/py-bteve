import colorsys
import random
import math
import gameduino2.prep
import zlib
import struct
import bteve as eve

from PIL import Image
import common

class Renderer(common.Branded):
    def __init__(self, gd):
        self.gd = gd
        self.t = 0

    def load(self):
        gd = self.gd

        ld = common.Loader(self.gd)
        # ld.add(struct.pack("4I", self.version, 0, 0, 0))
        self.subload(ld)


    def subload(self, ld):
        self.angle = 45
        self.av = 0

        gd = self.gd

        gd.cmd_flashfast()
        print("Flash fast: %04x" % gd.result())

        ttfname = "/home/jamesb/.fonts/Commodore Pixelized v1.2.ttf"
        self.textload(ld, ttfname, 0.7)

        print('end', hex(ld.a))

        gd.BitmapHandle(9)
        checker = Image.frombytes("L", (2, 2), bytes([255, 0, 0, 255]))
        ld.L8(checker)
        gd.BitmapSize(eve.NEAREST, eve.REPEAT, eve.REPEAT, 0, 0)

        jb = Image.open("assets/walk.png")
        im = Image.new("RGBA", (32, 32 * 9))
        for i in range(9):
            im.paste(jb.crop((32 * i, 0, 32 * i + 32, 32)), (0, 32 * i))
        fim = im.transpose(Image.FLIP_LEFT_RIGHT)

        for (h, i) in ((10, im), (11, fim)):
            gd.BitmapHandle(h)
            ld.ARGB4(i)
            gd.BitmapSize(eve.NEAREST, eve.BORDER, eve.BORDER, 3 * 32, 3 * 32)
            gd.BitmapLayout(eve.ARGB4, 64, 32)

        self.t = 0

    def draw(self):
        gd = self.gd

        gd.VertexFormat(3)
        gd.cmd_gradient(0, 700, 0x004000, 0, 0, 0x0000a0)

        gd.Begin(eve.BITMAPS)
        gd.ColorRGB(0x80, 0x80, 0)
        gd.SaveContext()
        gd.cmd_loadidentity()
        gd.cmd_scale(3, 3)
        gd.cmd_setmatrix()
        gd.Vertex2ii(0, 0, 9)

        g = 0xe0
        gd.ColorRGB(g, g, g)
        gd.Cell((self.t // 4) % 9)
        for j in range(6):
            gd.BitmapHandle(10 + (j & 1))
            d = 1 - 2 * (j & 1)
            for i in range(9):
                x = -96 + (i * 160 + 80 * (j & 1) + self.t * d) % (1280 + 160)
                y = j * 120
                gd.Vertex2f(x, y)

        gd.RestoreContext()

        gd.BitmapHandle(9)
        # [o.draw(gd) for o in self.obj]
        # [o.move() for o in self.obj]

        gd.SaveContext()
        gd.VertexTranslateX(16 * 10)
        gd.VertexTranslateY(16 * 10)
        gd.ColorRGB(0, 0, 0)
        self.textdraw()
        gd.RestoreContext()

        gd.ColorRGB(0xff, 0xff, 0xff)
        self.textdraw()

        self.t += 1
