import sys
import array
import random
import math
import gameduino2.prep
import zlib
import struct
import gameduino as GD
from eve import align4

from PIL import Image
import numpy as np
import wave
import common

GLOWR = (128, 256)
GLOWR = (160, 400)

sys.path.append("/home/jamesb/git/gd2-asset/examples/nightstrike")
import night0

class Renderer(common.Branded):
    def __init__(self, eve):
        self.eve = eve
        self.t = 0

    def load(self):
        eve = self.eve

        eve.cc(open("/home/jamesb/git/gd2-asset/examples/nightstrike/night0.gd3", "rb").read())

    def draw(self):
        eve = self.eve

        eve.VertexFormat(3)
        eve.ClearColorRGB(0, 0, 100)
        eve.Clear()

        eve.Begin(GD.BITMAPS)
        eve.BlendFunc(GD.SRC_ALPHA, 0)

        night0.missile_a.draw(eve, 640, 360, 2, angle = self.t)
        self.t += 1
