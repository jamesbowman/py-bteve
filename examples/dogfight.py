from PIL import Image, ImageFont, ImageDraw, ImageChops
import zlib
import math
import random
import colorsys

import vectormath as vmath

import registers as gd3
from gameduino2.convert import convert
from eve import EVE, align4

random.seed(0)

D = 56
SZ = 2 * (2 * D) ** 2

rr = random.randrange

def flash(fd, atlas):
    spr = bytes([int(x) for x in open("spr0", "rt")])
    atlas['ships'] = len(fd)
    sz = 4 * (2 * D) ** 2
    for i in range(256):
        print(i)
        bb = spr[sz*i:sz*(i+1)]
        sd = Image.frombytes("RGBA", (2 * D, 2 * D), bb)
        (b, g, r, a) = sd.split()
        sd = Image.merge("RGBA", (r, g, b, a))
        # sd.save("%04d.png" % i)
        co = convert(sd, True, gd3.ARGB4)[1]
        b = co.tobytes()
        fd += b
    return (fd, atlas)

class Shot:
    def __init__(self, pos, vel, rgb):
        self.pos = pos
        self.vel = vel
        self.rgb = rgb

    def move(self):
        self.pos += self.vel
        return self

    def draw(self, gd):
        v = self.vel

        gd.ColorRGB(*self.rgb)
        def line():
            gd.Vertex2f(*self.pos)
            gd.Vertex2f(*(self.pos + 4 * v))

        gd.ColorA(100)
        gd.LineWidth(100)
        line()
        gd.ColorA(255)
        gd.LineWidth(26)
        line()

    def is_alive(self):
        return (0 < self.pos.x < 1280) and (0 < self.pos.y < 720)

class Spark:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.age = 0

    def move(self):
        self.pos += self.vel
        self.age += 1 / 10
        return self

    def draw(self, gd):
        v = self.vel

        gd.Vertex2f(*self.pos)

    def is_alive(self):
        return self.age < 1

class Fighter:
    xc = 100

    def __init__(self, i):
        self.pos = vmath.Vector2(self.xc + rr(-500, 500), rr(720))
        self.i = i
        self.vel = vmath.Vector2(rr(-10, 10), rr(-10, 10)).as_unit()
        self.swiz = [gd3.RED, gd3.GREEN, gd3.BLUE]
        random.shuffle(self.swiz)
        self.rgb = [(0x3e, 0x86, 0x6e)[i - gd3.RED] for i in self.swiz]
        self.swiz += [gd3.ALPHA]

    def move(self):
        ax = [1, -1][self.pos.x > self.xc]
        ay = [1, -1][self.pos.y > 360]
        acc = vmath.Vector2(ax, ay).as_length(0.3)
        self.vel += acc
        self.pos += self.vel

    def draw(self, gd, ships, addr):
        v = self.vel.as_unit()
        a = int(256 * math.atan2(-v.x, v.y) / (2 * math.pi)) & 0xfe
        slot = addr + self.i * SZ
        gd.cmd_flashread(slot, 8192 + SZ * a, SZ)

        gd.Begin(gd3.BITMAPS)
        gd.BitmapSource(slot)
        gd.BitmapSwizzle(*self.swiz)
        gd.Vertex2f(*(self.pos - vmath.Vector2(D, D)))

    def draw2(self, gd, _):
        gd.Begin(gd3.POINTS)
        gd.PointSize(150)
        gd.Vertex2f(*self.pos)

    def fire(self):
        return Shot(self.pos.copy(), self.vel.as_length(50), self.rgb)

    def spark(self):
        p = self.pos
        d = self.vel.as_unit()
        r = vmath.Vector2(random.choice([-3,-2,-1,1,2,3]), random.choice([-3,-2,-1,1,2,3])).as_length(1)
        return Spark(p - d.as_length(20), self.vel - 8 * d + r)

class Dogfight():
    def __init__(self, atlas, addr):
        self.ships = atlas['ships']
        self.fi = [Fighter(i) for i in range(16)]
        self.sh = []
        self.sp = []
        self.t = 0
        for i in range(1000):
            self.move()
        self.addr = addr

    def move(self):
        self.sp = [s.move() for s in self.sp if s.is_alive()]
        self.sh = [s.move() for s in self.sh if s.is_alive()]
        [f.move() for f in self.fi if f]
        if 1 and (rr(6) == 0):
            self.sh.append(random.choice(self.fi).fire())
        for f in self.fi:
            self.sp.append(f.spark())
            self.t += 1

    def run(self, gd):
        gd.cmd_setbitmap(0, gd3.ARGB4, 2*D, 2*D)
        gd.BitmapLayout(gd3.GLFORMAT, 4*D, 2*D);
        gd.BitmapExtFormat(gd3.ARGB4);

        gd.SaveContext()
        gd.ColorRGB(0x80, 0x40, 0x20)
        gd.PointSize(80)
        gd.BlendFunc(gd3.SRC_ALPHA, 1)
        gd.Begin(gd3.POINTS)
        [s.draw(gd) for s in self.sp]
        gd.RestoreContext()

        [f.draw(gd, self.ships, self.addr) for f in self.fi]

        gd.Begin(gd3.LINES)
        gd.BlendFunc(gd3.SRC_ALPHA, 1)

        [s.draw(gd) for s in self.sh]

        self.move()
