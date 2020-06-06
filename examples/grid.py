import random
from gameduino_spidriver import GameduinoSPIDriver
import registers as gd3
from PIL import Image, ImageFont, ImageDraw, ImageChops
from eve import align4, EVE
import zlib
import numpy as np

def gentext(s, h):
    fn = "../../.fonts/IBMPlexSans-SemiBold.otf"
    fn = "../../.fonts/Arista-Pro-Alternate-Light-trial.ttf"
    font = ImageFont.truetype(fn, h)
    im = Image.new("L", (8000, 1000))
    draw = ImageDraw.Draw(im)
    draw.text((1, 1), s, font=font, fill = 255)
    return im.crop(im.getbbox())

    glow = im.filter(ImageFilter.GaussianBlur(10))
    im = ImageChops.add(im, glow)
    return im.crop(im.getbbox())


if __name__ == "__main__":
    gd = GameduinoSPIDriver()
    gd.init()

    bg = Image.open("../povray/stripes60.png").convert("L").crop((0, 0, 1280, 360))
    a = 0

    gd.cmd_inflate(a)
    gd.cc(align4(zlib.compress(bg.tobytes())))
    gd.cmd_setbitmap(a, gd3.L8, 1280, 360)
    a += (1280 * 360)

    def slice(i):
        im = Image.open("../povray/stripes%02d.png" % i).convert("L").crop((640, 0, 641, 720))
        return im.tobytes()

    slices = b"".join([slice(i) for i in range(60)])

    gd.BitmapHandle(1)
    gd.cmd_inflate(a)
    gd.cc(align4(zlib.compress(slices)))
    gd.cmd_setbitmap(a, gd3.L8, 1, 720)
    gd.BitmapSize(gd3.NEAREST, gd3.REPEAT, gd3.BORDER, 1280, 720)
    gd.BitmapSizeH(1280 >> 9, 720 >> 9)
    a += (60 * 720)

    def norm(v):
        return v / max(v)

    def gauss(r):
        w = 2 * r
        x = np.tile(np.linspace(-1, 1, w), 1)
        c = np.sqrt(.04)
        gauss_x = np.exp(-(x*x) / (2 * c ** 2))
        t = gauss_x
        return (255 * t).astype(np.uint8).reshape(w, 1).tobytes()

    pattern = gauss(360)
    gd.BitmapHandle(2)
    gd.cmd_inflate(a)
    gd.cc(align4(zlib.compress(pattern)))
    gd.cmd_setbitmap(a, gd3.L8, 1, 720)
    gd.BitmapSize(gd3.NEAREST, gd3.REPEAT, gd3.BORDER, 1280, 720)
    gd.BitmapSizeH(1280 >> 9, 720 >> 9)
    a += (1 * 720)

    pattern = gentext("dazzler", 300)
    (w, h) = pattern.size
    gd.BitmapHandle(3)
    gd.cmd_inflate(a)
    gd.cc(align4(zlib.compress(pattern.tobytes())))
    gd.cmd_setbitmap(a, gd3.L8, w, h)
    a += w * h

    print(a)

    for i in range(2000):
        gd.VertexFormat(0)
        gd.Clear()

        gd.Begin(gd3.BITMAPS)
        gd.ColorRGB(0, 0x20, 0x20)
        gd.Vertex2ii(0, 0, 2, 0)
        gd.ColorRGB(0xff, 0xa5, 0x00)

        if 1:
            gd.SaveContext()
            gd.BitmapHandle(0)
            gd.Vertex2f(0, 0)
            gd.cmd_translate(1280, 360)
            gd.cmd_scale(-1, -1)
            gd.cmd_setmatrix()
            gd.Vertex2f(0, 360)
            gd.RestoreContext()

        gd.BitmapHandle(1)
        gd.Cell((3 * i) % 60)
        gd.Vertex2f(0, 0)

        gd.ColorRGB(255, 255, 255)
        gd.Cell(0)
        gd.BitmapHandle(3)
        gd.Vertex2f(640 - w / 2, 330 - h / 2)

        gd.swap()
