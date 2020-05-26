import os
import time
from gameduino_spidriver import GameduinoSPIDriver
import registers as gd3
from eve import align4

class VideoPlayer:
    def __init__(self, gd, mf_base, mf_size):
        self.gd = gd
        self.mf_base = mf_base
        self.mf_size = mf_size

        self.running_flag = mf_base - 4

        gd.cmd_regwrite(self.running_flag, 1)
        gd.cmd_mediafifo(mf_base, mf_size)
        self.wp = 0
        gd.cmd_regwrite(gd3.REG_MEDIAFIFO_WRITE, 0)

    def start(self, fn, sz):
        gd = self.gd

        scale_factor = 1280 / sz[0]
        gd.Clear()
        gd.cmd_setbitmap(0, gd3.RGB565, sz[0], sz[1])
        gd.BitmapSize(gd3.BILINEAR, gd3.BORDER, gd3.BORDER, 1280, 720)
        gd.BitmapSizeH(1280 >> 9, 720 >> 9)
        gd.Begin(gd3.BITMAPS)
        gd.cmd_scale(scale_factor, scale_factor)
        gd.cmd_setmatrix()
        h = sz[1] * scale_factor
        gd.Vertex2f(0, (720 - h) / 2)
        gd.swap()
        gd.cmd_videostart()

        self.vf = open(fn, "rb")
        
    def service(self):
        gd = self.gd

        rp = gd.rd32(gd3.REG_MEDIAFIFO_READ)
        fullness = (self.wp - rp) % self.mf_size
        SZ = 2048
        while fullness < (self.mf_size - SZ):
            sector = self.vf.read(SZ)
            gd.wr(self.mf_base + self.wp, sector)
            self.wp = (self.wp + len(sector)) % self.mf_size
            gd.wr32(gd3.REG_MEDIAFIFO_WRITE, self.wp)
            fullness += len(sector)

    def single(self):
        gd = self.gd

        gd.cmd_videoframe(0, self.running_flag)
        gd.flush()
        while not gd.is_idle():
            self.service()
        return gd.rd32(self.running_flag)

if __name__ == "__main__":
    gd = GameduinoSPIDriver()
    gd.init()
    time.sleep(8)

    (fn, sz) = ("jellyfish.avi", (960, 540))
    (fn, sz) = ("chickens-4.avi", (854, 480))
    (fn, sz) = ("tree.avi", (960, 506))

    vp = VideoPlayer(gd, 0xfe000, 0x2000)
    vp.start(fn ,sz)

    t0 = time.time()
    while vp.single():
        print("frame")
        os.system("ptpcam -c")
    t1 = time.time()
    print('took', t1 - t0)
