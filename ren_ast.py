import colorsys
import random
import math
import gameduino2.prep
import zlib
import struct
import gameduino as GD
from eve import align4

class Asteroid:
    def __init__(self, i):
        self.i = i
        self.x = random.randrange(1280)
        self.y = random.randrange(720)
        self.w = random.choice((-1, 1)) * random.randrange(60, 120) / 100
        self.a = random.randrange(128)
        self.kind = random.randrange(2)
        th = math.pi * 2 * random.random()
        v = 1 + 2 * random.random()
        self.vx = v * math.sin(th)
        self.vy = v * math.cos(th)
        self.p = 0

    def draw(self, eve):
        C = 0x2400
        addr = 8192 + (2 * self.i + self.p) * C
        eve.cmd_flashread(addr, 8192 + (128 * self.kind + (int(self.a) & 127)) * C, C)
        eve.BitmapSource(addr)
        eve.Vertex2f(self.x, self.y)
        self.p ^= 1

    def move(self):
        self.a += self.w
        self.x += self.vx
        self.y += self.vy
        D = 192
        if self.x < -D:
            self.x += (1280 + D)
        if self.x > 1280:
            self.x -= (1280 + D)
        if self.y < -D:
            self.y += (720 + D)
        if self.y > 720:
            self.y -= (720 + D)

class Renderer:
    def __init__(self, eve):
        self.eve = eve

        eve.cmd_flashfast()
        print("Flash fast: %04x" % eve.result())
        eve.cmd_memcpy(0xffff0, GD.REG_CLOCK, 4)
        eve.cmd_flashread(0, 4096, 4096)
        eve.cmd_memcpy(0xffff4, GD.REG_CLOCK, 4)
        eve.finish()
        (t0,t1) = struct.unpack("II", eve.rd(0xffff0, 8))
        print('flash read took', t1 - t0, eve.rd32(GD.REG_FLASH_STATUS))

        eve.cmd_setbitmap(0, GD.ASTC_8x8, 192, 192)
        eve.BitmapSwizzle(GD.RED, GD.GREEN, GD.BLUE, GD.ALPHA)

        random.seed(7)
        self.t = 0
        self.obj = [Asteroid(i) for i in range(10)]

        eve.BitmapHandle(1)
        (bw, bh, d) = gameduino2.prep.astc_tile(open("stars.astc", "rb"))
        eve.cmd_inflate(0x80000)
        eve.cc(align4(zlib.compress(d)))
        eve.cmd_setbitmap(0x80000, GD.ASTC_12x12, 2048, 1024)

        self.angle = 45
        self.av = 0

    def draw(self):
        eve = self.eve

        eve.finish()
        (wii1, wii2) = self.eve.controllers()

        eve.VertexFormat(3)
        if 0:
            eve.ClearColorRGB(10, 10, 20)
            eve.Clear()

        eve.Begin(GD.BITMAPS)
        eve.Vertex2ii(0, 0, 1, 0)

        # eve.cmd_loadidentity()
        # eve.cmd_rotate_around(640, 360, self.t)
        # eve.cmd_setmatrix()
        eve.BitmapHandle(0)
        if 1:
            [o.draw(eve) for o in self.obj]
            [o.move() for o in self.obj]
        else:
            C = 0x2400
            eve.cmd_flashread(0, 8192 + (int(self.t) & 127) * C, C)
            eve.BitmapSource(0)
            eve.Vertex2f(100, 100)

            eve.cmd_flashread(C, 8192 + (128 + (int(self.t) & 127)) * C, C)
            eve.BitmapSource(C)
            eve.Vertex2f(700, 100)

        eve.cmd_dial(eve.w // 2, eve.h // 2, 100, 0, self.angle)

        af = 0.5 * (wii1["lx"] - 32) / 32
        self.av = 0.9 * (self.av + af)
        self.angle += self.av

        self.t += 1
