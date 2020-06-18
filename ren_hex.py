import GD
import colorsys
import random
import math
import gameduino2.prep
import zlib
import numpy as np
from PIL import Image
from PIL import ImageFilter

class Renderer:
    def __init__(self, eve):
        self.eve = eve
        self.t = 0

    def load(self):
        pass

    def draw(self):
        eve = self.eve
        self.im = (Image.open("assets/dance/%04d.png" % max(1, self.t)).
                  convert("L").
                  filter(ImageFilter.GaussianBlur(10)).
                  resize((1281, 721), Image.BICUBIC).
                  load())
        self.t += 1

        eve.VertexFormat(3)
        eve.ClearColorRGB(255, 255, 255)
        eve.Clear()
        eve.ColorRGB(0, 0, 0)
        eve.Begin(GD.POINTS)
        N = 50
        r = 1280 / (N - 1)
        msize = int(7.8 * r)    # maximum point size
        eve.PointSize(msize)
        h = 0.5 * r / math.tan(math.pi / 6)
        M = int(math.ceil(720 / h))

        print('pointsize', int(7*r))
        print('r', r)
        print('h', h)

        allp = [(x * r, y * h) for x in range(N) for y in range(0, M, 2)]
        allp += [((x + 0.5) * r, y * h) for x in range(N - 1) for y in range(1, M, 2)]

        def sample(x, y):
            i = 1 - self.im[int(x), int(y)] / 255
            i = 0.2 + 0.8 * i
            Q = 60
            return msize * int(Q * i) // Q
        sxy = [(sample(x, y), x, y) for (x, y) in allp]
        bysz = {}
        for (s,x,y) in sxy:
            if not s in bysz:
                bysz[s] = []
            bysz[s].append((x,y))
        for s,xy in bysz.items():
            eve.PointSize(s)
            for (x, y) in xy:
                eve.Vertex2f(x, y)
