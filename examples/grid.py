import sys
import random
from gameduino_spidriver import GameduinoSPIDriver
import registers as gd3
from PIL import Image, ImageFont, ImageDraw, ImageChops, ImageFilter
from eve import align4, EVE
import zlib
import numpy as np
from scipy.ndimage import gaussian_filter

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

def norm(v):
    return v / np.amax(v)

def glow(r):
    w = 2 * r
    x = np.tile(np.linspace(-1, 1, w), w)
    y = np.repeat(np.linspace(-1, 1, w), w)
    c = np.sqrt(.10)
    gauss_x = np.exp(-(x*x) / (2 * c ** 2))
    gauss_y = np.exp(-(y*y) / (2 * c ** 2))
    t = norm(gauss_x * gauss_y)
    ti = (255 * t).astype(np.uint8).reshape(w, w)
    return Image.fromarray(ti, "L")

def gauss(r):
    w = 2 * r
    x = np.tile(np.linspace(-1, 1, w), 1)
    c = np.sqrt(.04)
    gauss_x = np.exp(-(x*x) / (2 * c ** 2))
    t = gauss_x
    return Image.frombytes("L", (1, w), (255 * t).astype(np.uint8).reshape(w, 1).tobytes())

class Loader:
    def __init__(self, gd, a = 0):
        self.gd = gd
        self.a = a

    def L8(self, im):
        (w, h) = im.size
        gd.cmd_inflate(self.a)
        d = im.tobytes()
        gd.cc(align4(zlib.compress(d)))
        gd.cmd_setbitmap(self.a, gd3.L8, w, h)
        self.a += len(d)

if __name__ == "__main__":
    dazzler_logo = gentext("dazzler", 300)
    print(dazzler_logo)
    f = 20
    dz = dazzler_logo.resize((949 // f, 195 // f)).convert("1")
    print(sum(dz.tobytes()) / 255)
    dz.save("out.png")
    pix = dz.load()
    spots = [((x + 1.0) * f, (y + 1.0) * f) for x in range(dz.size[0]) for y in range(dz.size[1]) if pix[x, y]]
    print((spots))

    (w, h) = dazzler_logo.size

    if 0:
        im = Image.new("L", (1280, 720))
        im.paste(dazzler_logo, (640 - w // 2, 330 - h // 2))
        im = im.resize((640, 360), Image.BICUBIC)
        fi = np.array(im).astype(np.float)
        g0 = gaussian_filter(fi, sigma = 12)
        g1 = gaussian_filter(fi, sigma = 75)
        dith = np.random.random_sample(g0.shape)
        g = (norm(g0 + g1 / 4) * 255 + dith).astype(np.uint8)
        im = Image.fromarray(g)
        # im = im.filter(ImageFilter.GaussianBlur(200))
        im.save("gaussblur.png")
        sys.exit(0)

    gd = GameduinoSPIDriver()
    gd.init()

    ld = Loader(gd, 0)

    bg = Image.open("../povray/stripes60.png").convert("L").crop((0, 0, 1280, 360))
    ld.L8(bg)

    def slice(i):
        im = Image.open("../povray/stripes%02d.png" % i).convert("L").crop((640, 0, 641, 720))
        return im.tobytes()

    slices = Image.frombytes("L", (720, 60), b"".join([slice(i) for i in range(60)]))
    gd.BitmapHandle(1)
    a = ld.a
    ld.L8(slices)
    gd.cmd_setbitmap(a, gd3.L8, 1, 720)
    gd.BitmapSize(gd3.NEAREST, gd3.REPEAT, gd3.BORDER, 1280, 720)
    gd.BitmapSizeH(1280 >> 9, 720 >> 9)

    gd.BitmapHandle(2)
    ld.L8(gauss(360))
    gd.BitmapSize(gd3.NEAREST, gd3.REPEAT, gd3.BORDER, 1280, 720)
    gd.BitmapSizeH(1280 >> 9, 720 >> 9)

    gd.BitmapHandle(3)
    ld.L8(dazzler_logo)

    gd.BitmapHandle(4)
    gr = 64
    ld.L8(glow(gr))

    gd.BitmapHandle(5)
    ld.L8(Image.open("gaussblur.png"))

    print(gd.rd32(gd3.REG_ADAPTIVE_FRAMERATE))

    rr = [
        "REG_HCYCLE",
        "REG_HOFFSET",
        "REG_HSIZE",
        "REG_HSYNC1",
        "REG_HSYNC0",
        "REG_VCYCLE",
        "REG_VOFFSET",
        "REG_VSIZE",
        "REG_VSYNC1",
        "REG_VSYNC0",
    ]
    # gd.wr32(gd3.REG_PCLK_POL, 1)

    for r in rr:
        print("%16s %d" % (r, gd.rd32(eval("gd3." + r))))

    for i in range(1):
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
        (ox, oy) = (640 - w / 2, 330 - h / 2)
        gd.Vertex2f(ox, oy)

        gd.BitmapHandle(4)
        gd.ColorRGB(255, 0, 0)
        gd.ColorA(255)
        for (x, y) in spots[:]:
            gd.Vertex2f(ox + x - gr, oy + y - gr)
            # gd.Vertex2f(ox + x - gr, oy + y - gr)

        gd.swap()
