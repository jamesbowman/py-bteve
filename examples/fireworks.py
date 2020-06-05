from PIL import Image, ImageFont, ImageDraw, ImageChops
import zlib
import math
import random
import colorsys
import numpy as np
import time

import vectormath as vmath

import registers as gd3
from gameduino2.convert import convert
from eve import EVE, align4

random.seed(0)

rr = random.randrange
ru = random.uniform

def norm(v):
    return v / max(v)

def glow(r):
    w = 2 * r
    x = np.tile(np.linspace(-1, 1, w), w)
    y = np.repeat(np.linspace(-1, 1, w), w)
    c = np.sqrt(.10)
    gauss_x = np.exp(-(x*x) / (2 * c ** 2))
    gauss_y = np.exp(-(y*y) / (2 * c ** 2))
    t = norm(gauss_x * gauss_y)
    ti = (255 * t).astype(np.uint8).reshape(w, w)
    return Image.fromarray(ti, "L")

def rot():
    a = ru(0, 2 * math.pi)
    return vmath.Vector2(math.sin(a), math.cos(a))

class Spark:
    def __init__(self, pos, vel, rgb, age):
        self.pos = pos
        self.vel = vel
        self.rgb = rgb
        self.age = age

    def move(self):
        self.vel.y += 0.12
        self.pos += self.vel
        if self.vel.y > 0:
            self.age += 1 / 10
            if self.age > 1:
                self.age = -999
                e = rot().as_length(ru(3, 5))
                self.vel += e
        return self.pos.y < 720

    def draw(self, gd):
        if gd.rgb != self.rgb:
            gd.ColorRGB(*self.rgb)
            gd.rgb = self.rgb
        gd.Vertex2f(*self.pos)

class Fireworks():
    xc = 3000
    r = 14
    def __init__(self, gd, atlas):
        im = glow(self.r)
        im.save("out.png")
        addr = atlas['ram']
        gd.cmd_inflate(addr)
        gd.cc(align4(zlib.compress(im.tobytes())))
        self.addr = addr
        self.t = 0
        atlas['ram'] = addr + len(im.tobytes())

        self.sparks = []

    def make(self):
        def color():
            rgb = [rr(0xe0, 0xff), rr(0x80, 0xf0), rr(0x40, 0xf0)]
            random.shuffle(rgb)
            return rgb
        colors = [color(), color()]
        x = self.xc + rr(-400, 400)
        age = ru(0, 0.2)
        v = vmath.Vector2(ru(-1, 1), ru(-11, -13))
        return [Spark(vmath.Vector2(x, 715) + rot().as_length(4),
                      v + rot().as_length(.1),
                      colors[i // 60],
                      age)
                for i in range(120)]
            
    def move(self):
        self.sparks = [s for s in self.sparks if s.move()]
        if (self.t % 30) == 0:
            self.sparks += self.make()
        self.t += 1

    def run(self, gd):
        gd.cmd_setbitmap(self.addr, gd3.L8, 2 * self.r, 2 * self.r)
        gd.Begin(gd3.BITMAPS)
        gd.BlendFunc(gd3.SRC_ALPHA, 1)
        gd.rgb = None
        [s.draw(gd) for s in self.sparks]

        self.move()
        self.move()
