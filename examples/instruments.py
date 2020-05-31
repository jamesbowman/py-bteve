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
        self.v = [rr(1000) for i in range(6)]

    def run(self, gd):
        h = 720 + 144
        for i,v in enumerate(self.v):
            y = -72 + (i * h // 5)
            gd.cmd_gauge(self.xc, y, h // 12, gd3.OPT_FLAT, 4, 2, v, 1000)
