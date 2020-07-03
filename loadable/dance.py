import random
import math
import zlib
import time
import numpy as np
from PIL import Image
from PIL import ImageFilter

from gameduino_spidriver import GameduinoSPIDriver
import registers as gd3
import common
from common import Pt

def fade(ti, sxy):
    H = 50
    if ti == 0:
        return []
    if ti > H:
        return sxy

    t = (ti / H)
    sxy = [(b, Pt(*xy)) for (b, xy) in sxy]
    center = Pt(720, 360)
    def xform(p):
        p -= center
        d = p.mag() / 500
        p = common.lerp(common.smoothstep(min(1.0, 1.3 * math.pow(t, d))), p * 5, p)
        p += center
        return p
        
    return [(b, xform(p).tuple()) for (b, p) in sxy]

class Renderer:
    def __init__(self, gd):
        self.gd = gd
        self.t = 0

    def load(self):
        gd = self.gd

        # gd.ClearColorRGB(0, 255, 0)
        # gd.Clear()
        # gd.swap()

        ld = common.Loader(gd)
        gd.BitmapHandle(0)
        ld.L8(Image.open("assets/caustics.png"))
        self.gd.cmd_setbitmap(0, gd3.L8, 128, 128)
        gd.BitmapSize(gd3.NEAREST, gd3.REPEAT, gd3.REPEAT, 0, 0)

    def load_1(self):
        gd = self.gd
        ALLMEM = 1 << 20
        def crc():
            gd.cmd_memcrc(0, ALLMEM, 0)
            return gd.result()

        gd.cmd_memzero(0, ALLMEM)
        print(crc())
        self.load()
        print(crc())
        
    def draw(self):
        gd = self.gd

        frame = self.t % 280
        self.im = (Image.open("assets/dance/%04d.png" % max(1, frame)).
                  convert("L").
                  filter(ImageFilter.GaussianBlur(10)).
                  # resize((1281, 721), Image.BICUBIC).
                  load())
        self.t += 1

        h0 = math.fmod(self.t * 0.013, 1.0)
        h1 = math.fmod(h0 + .5, 1.0)
        sat = .4
        gd.VertexFormat(2)
        gd.ClearColorRGB(*common.hsv(h0, .3, .9))
        gd.Clear()

        gd.BitmapHandle(0)
        gd.Begin(gd3.BITMAPS)
        gd.cmd_scale(8, 4)
        gd.cmd_setmatrix()
        gd.Cell(self.t % 32)
        gd.ColorRGB(*common.hsv(h1, .4, 1))
        gd.Vertex2f(0, 0)

        gd.ColorRGB(0, 0, 0)
        gd.Begin(gd3.POINTS)
        N = 50
        r = 1280 / (N - 1)
        msize = int(7.8 * r)    # maximum point size
        gd.PointSize(msize)
        h = 0.5 * r / math.tan(math.pi / 6)
        M = int(math.ceil(720 / h))

        # print('pointsize', int(7*r))
        # print('r', r)
        # print('h', h)

        allp = [(x * r, (y + 0.4) * h) for x in range(N) for y in range(0, M, 2)]
        allp += [((x + 0.5) * r, (y + 0.4) * h) for x in range(N - 1) for y in range(1, M, 2)]

        def sample(x, y):
            i = 1 - self.im[min(1279, int(x)), min(719, int(y))] / 255
            i = 0.1 + 0.8 * i
            Q = 60
            return (msize * int(Q * i) // Q) & ~3
        sxy = [(sample(x, y), (x, y)) for (x, y) in allp]

        sxy = fade(max(0, self.t - 30), sxy)

        bysz = {}
        for (s,xy) in sxy:
            if not s in bysz:
                bysz[s] = []
            bysz[s].append(xy)
        for s,xy in bysz.items():
            gd.PointSize(s)
            for (x, y) in xy:
                gd.Vertex2f(x, y)

        gd.RestoreContext()
        # gd.cmd_number(0, 0, 31, 3, frame);
