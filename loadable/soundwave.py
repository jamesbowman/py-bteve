import array
import random
import math
import gameduino2.prep
import zlib
import struct
import gameduino as GD
from eve import align4

from PIL import Image
import wave
import common

class Renderer(common.Branded):
    def __init__(self, eve):
        self.eve = eve
        self.t = 0

    def load(self):
        eve = self.eve

        ld = common.Loader(self.eve)
        # ld.add(struct.pack("4I", self.version, 0, 0, 0))
        self.subload(ld)
    
        self.wave = wave.open("track4.wav", "rb")
        NF = 700
        self.wave.readframes(NF * 44100 // 30)

    def subload(self, ld):
        self.t = 0

    def draw(self):
        eve = self.eve

        eve.VertexFormat(3)
        eve.cmd_gradient(0, 700, 0x004000, 0, 0, 0x0000a0)

        eve.Begin(GD.BITMAPS)
        f0 = self.t * 44100 // 30
        f1 = (1 + self.t) * 44100 // 30
        n = (f1 - f0)
        samples = np.frombuffer(self.wave.readframes(n), np.int16).reshape(2, n) / 32767
        for ch in (0, 1):
            im = Image.fromarray("L", (samples[ch] * 255).astype(


        self.t += 1
