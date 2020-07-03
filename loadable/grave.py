
import sys
import datetime
from datetime import timezone
import time
import math
import struct
import numpy as np

from PIL import Image
from gameduino_spidriver import GameduinoSPIDriver
import registers as gd3
import common
import gameduino2.prep
import gameduino2.convert

import tmxreader

TD = 86

class Renderer:
    
    def __init__(self, gd):
        self.gd = gd
        self.t = 0

    version = 102

    def load(self):
        gd = self.gd

        Mloc = 0
        if gd.rd32(Mloc) != self.version:
            ld = common.Loader(gd)
            ld.add(struct.pack("4I", self.version, 0, 0, 0))
            self.subload(ld)

    def fetchtile(self, l, i, j):
        world_map = self.world_map
        used = self.used
        def reindex(i):
            if i == 0:
                return None
            else:
                return used.index(i)
        if (i < world_map.width) and (j < world_map.height):
            return reindex(l.decoded_content[i + (j * world_map.width)])
        else:
            return None

    def subload(self, ld):

        gd = self.gd
        world_map = tmxreader.TileMapParser().parse_decode("../tiled-maps/grave.tmx")
        print(world_map.tile_sets[0].images[0].source)
        used = list(sorted(set(sum([list(l.decoded_content) for l in world_map.layers], [])) - {0}))
        print('used', used)

        self.world_map = world_map
        self.used = used

        ts = world_map.tile_sets[0]
        tw = int(ts.tilewidth)
        th = int(ts.tileheight)
        im = (Image.open(world_map.tile_sets[0].images[0].source))
        def extract(i):
            if hasattr(ts, 'columns'):
                w = int(ts.columns)
            elif not hasattr(ts, 'spacing'):
                w = im.size[0] // tw
            else:
                w = (im.size[0] + ts.spacing) // (tw + ts.spacing)
            x = ts.margin + (tw + ts.spacing) * (i % w)
            y = ts.margin + (th + ts.spacing) * (i // w)
            print(i, 'is at', (x, y))
            r = im.crop((x + 0, y + 0, x + tw, y + th))
            r.save("x%d.png" % i)
            if 0 and scale:
                r = r.resize((stw, sth), Image.ANTIALIAS)
            return r

        if 0:
            for ti in used:
                t = extract(ti).resize((90, 90), Image.BICUBIC)
                print(ti, t)

        gd.BitmapHandle(0)
        ld.Lastc("grave-moon.astc")
        gd.BitmapHandle(1)
        ld.L4(Image.open("grave-bg0.png").convert("L"))
        gd.BitmapSize(gd3.BILINEAR, gd3.REPEAT, gd3.BORDER, 1280, 95)

        tilebase = ld.a

        gd.BitmapHandle(2)
        if 1:
            for ti in used:
                ti -= 1
                print('loading', ti)
                t = extract(ti).resize((TD, TD), Image.BICUBIC)
                (_, d) = gameduino2.convert.convert(t, False, gd3.ARGB4)
                ld.add(d)
        gd.cmd_setbitmap(tilebase, gd3.ARGB4, TD, TD)

        h = 120
        walks = []
        for i in range(1, 11):
            walk = Image.open("zombie/Walk (%d).png" % i).resize((430 * h // 519, h), Image.BILINEAR)
            walks.append(walk)

        gd.BitmapHandle(3)
        ld.ARGB4s(walks)
        print('end', hex(ld.a))

    def draw(self):
        gd = self.gd

        gd.Clear()
        gd.SaveContext()
        gd.ScissorSize(1280, 460)
        gd.cmd_gradient(0, 0, 0x1a1a1a, 0, 400, 0x193439)
        gd.RestoreContext()

        gd.VertexFormat(3)
        gd.Begin(gd3.BITMAPS)

        gd.BitmapHandle(0)
        gd.Vertex2f((1280 - 756) / 2, 40)

        sx = 2 * self.t

        def scale(n, rgb, y):
            gd.SaveContext()
            gd.cmd_scale(n, n)
            gd.cmd_translate((947 - sx / 2) * n, 0)
            gd.cmd_setmatrix()
            gd.cmd_loadidentity()
            gd.ColorRGB(*common.hex3(rgb))
            gd.Vertex2f(0, y)
            gd.ClearColorRGB(*common.hex3(rgb))
            gd.ScissorXY(0, y + 95)
            gd.Clear()
            gd.RestoreContext()

        if 1:
            gd.BitmapHandle(1)
            scale(0.6, 0x193439, 400)
            scale(0.8, 0x162a2d, 440)
            scale(1.0, 0x0d1516, 480)

        if 1:
            gd.BitmapHandle(2)
            tb = (sx // TD)
            y0 = 720 - 8 * TD
            for j in range(8):
                for i in range(16):
                    for l in self.world_map.layers:
                        ti = self.fetchtile(l, tb + i, 0 + j)
                        if ti is not None:
                            # print('draw', (i, j), ti)
                            gd.Cell(ti)
                            gd.Vertex2f(TD * i - sx % TD, y0 + TD * j)

        if 0:
            frame = (self.t // 4) % 10
            gd.BitmapHandle(3)
            gd.Cell(frame)
            for i in range(8):
                gd.Vertex2f(0, y0 + TD * i - 30)

        if 0:
            gd.Begin(gd3.LINES)
            gd.Vertex2f(0, 0)
            gd.Vertex2f(1280, 720)

        # gd.swap(); gd.screenshot_im().save("out.png") ; sys.exit(0)

        self.t += 2
        if self.t > 600:
            sys.exit(0)
        print(self.t)
