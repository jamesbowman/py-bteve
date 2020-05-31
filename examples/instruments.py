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

rr = random.randrange

class Instruments():
    xc = 1200
    def __init__(self, atlas, addr):
        self.va = rr(1000)
        self.ta = rr(1000)
        self.t = 0

    def run0(self, gd):
        h = 720 + 144
        for i,v in enumerate(self.v):
            y = -72 + (i * h // 5)
            gd.cmd_gauge(self.xc, y, h // 12, gd3.OPT_FLAT, 4, 2, v, 1000)
    
    def run(self, gd):
        if (self.t % 20) == 0:
            self.ta = rr(1000)
        e = self.ta - self.va
        self.va += 0.1 * e
        gd.cmd_gauge(858, 451, 180, gd3.OPT_FLAT, 4, 4, int(self.va), 1000)
        self.t += 1
