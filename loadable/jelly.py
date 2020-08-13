import colorsys
import random
import math
import gameduino2.prep
import zlib
import struct
import gameduino as GD
from eve import align4

from PIL import Image
import common

class Renderer(common.Branded):
    def __init__(self, eve):
        self.eve = eve
        self.t = 0

    def load(self):
        eve = self.eve

        ld = common.Loader(self.eve)
        # ld.add(struct.pack("4I", self.version, 0, 0, 0))
        self.subload(ld)


    def subload(self, ld):
        self.angle = 45
        self.av = 0

        eve = self.eve

        eve.cmd_flashfast()
        print("Flash fast: %04x" % eve.result())

        ttfname = "/home/jamesb/.fonts/Commodore Pixelized v1.2.ttf"
        self.textload(ld, ttfname, 0.7)

        print('end', hex(ld.a))

        eve.BitmapHandle(9)
        checker = Image.frombytes("L", (2, 2), bytes([255, 0, 0, 255]))
        ld.L8(checker)
        eve.BitmapSize(GD.NEAREST, GD.REPEAT, GD.REPEAT, 0, 0)

        jb = Image.open("assets/walk.png")
        im = Image.new("RGBA", (32, 32 * 9))
        for i in range(9):
            im.paste(jb.crop((32 * i, 0, 32 * i + 32, 32)), (0, 32 * i))
        fim = im.transpose(Image.FLIP_LEFT_RIGHT)

        for (h, i) in ((10, im), (11, fim)):
            eve.BitmapHandle(h)
            ld.ARGB4(i)
            eve.BitmapSize(GD.NEAREST, GD.BORDER, GD.BORDER, 3 * 32, 3 * 32)
            eve.BitmapLayout(GD.ARGB4, 64, 32)

        self.t = 0

    def draw(self):
        eve = self.eve

        eve.VertexFormat(3)
        eve.cmd_gradient(0, 700, 0x004000, 0, 0, 0x0000a0)

        eve.Begin(GD.BITMAPS)
        eve.ColorRGB(0x80, 0x80, 0)
        eve.SaveContext()
        eve.cmd_loadidentity()
        eve.cmd_scale(3, 3)
        eve.cmd_setmatrix()
        eve.Vertex2ii(0, 0, 9)

        g = 0xe0
        eve.ColorRGB(g, g, g)
        eve.Cell((self.t // 4) % 9)
        for j in range(6):
            eve.BitmapHandle(10 + (j & 1))
            d = 1 - 2 * (j & 1)
            for i in range(9):
                x = -96 + (i * 160 + 80 * (j & 1) + self.t * d) % (1280 + 160)
                y = j * 120
                eve.Vertex2f(x, y)

        eve.RestoreContext()

        eve.BitmapHandle(9)
        # [o.draw(eve) for o in self.obj]
        # [o.move() for o in self.obj]

        eve.SaveContext()
        eve.VertexTranslateX(16 * 10)
        eve.VertexTranslateY(16 * 10)
        eve.ColorRGB(0, 0, 0)
        self.textdraw()
        eve.RestoreContext()

        eve.ColorRGB(0xff, 0xff, 0xff)
        self.textdraw()

        self.t += 1
