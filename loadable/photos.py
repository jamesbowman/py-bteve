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
from common import Pt

class Renderer:
    
    def __init__(self, gd):
        self.gd = gd
        self.t = 0

    version = 100

    def load(self):
        gd = self.gd

        Mloc = 0
        if gd.rd32(Mloc) != self.version:
            ld = common.Loader(gd)
            ld.add(struct.pack("4I", self.version, 0, 0, 0))
            self.subload(ld)
        print(hex(gd.rd32(Mloc)))

    def subload(self, ld):
        gd = self.gd
        gd.BitmapHandle(0)
        # ld.Lastc("assets/landscape.astc")
        ld.Lastc("assets/italy.astc")
        gd.BitmapSize(gd3.BILINEAR, gd3.BORDER, gd3.BORDER, 1440, 810)
        gd.BitmapHandle(1)
        ld.Lastc("assets/elephant.astc")
        gd.BitmapSize(gd3.BILINEAR, gd3.BORDER, gd3.BORDER, 1440, 810)

    def draw(self):
        gd = self.gd

        gd.finish()

        if 1:
            v = 0x808f
            gd.cmd_regwrite(gd3.REG_GPIOX, v | (1 << 12))
            print(hex(gd.rd32(gd3.REG_GPIOX)))

        gd.Begin(gd3.BITMAPS)
        def swell(s):
            sf = common.map(s, 0, 1, 1280, 1440) / 1440
            gd.cmd_loadidentity()
            gd.cmd_translate(640, 360)
            gd.cmd_scale(sf, sf)
            gd.cmd_translate(-1440 / 2, -810 / 2)
            gd.cmd_setmatrix()


        t = self.t
        o = int(max(common.map(t, 80, 90, 255, 0),
                    common.map(t, 160, 170, 0, 255)))
        gd.BitmapHandle(0)
        gd.BlendFunc(gd3.SRC_ALPHA, 0)
        gd.ColorA(o)
        if t < 90:
            swell(common.map(t, 0, 90))
        else:
            swell(common.map(t, 160, 250))
        gd.Vertex2f(0, 0)

        if 1:
            o = int(min(common.map(t, 80, 90, 0, 255),
                        common.map(t, 160, 170, 255, 0)))
            gd.BitmapHandle(1)
            gd.BlendFunc(gd3.SRC_ALPHA, 1)
            gd.ColorA(o)
            swell(common.map(t, 80, 80 + 90))
            gd.Vertex2f(0, 0)

        gd.RestoreContext()
        # gd.cmd_number(0, 0, 29, 3, t)

        self.t += 1
        self.t %= 250
        assert self.t < 250
        # time.sleep(1/40)
