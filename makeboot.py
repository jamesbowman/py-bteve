import textwrap
import struct
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from _eve import _EVE
from eve import EVE, align4
import registers as gd3
import zlib
from io import BytesIO
from itertools import groupby
from gameduino2.convert import convert
import random

random.seed(7)
rr = random.randrange

__VERSION__ = "0.0.3"

def gentext(s):
    fn = "../../.fonts/IBMPlexSans-SemiBold.otf"
    fn = "../../.fonts/Arista-Pro-Alternate-Light-trial.ttf"
    font = ImageFont.truetype(fn, 250)
    im = Image.new("L", (2000, 1000))
    draw = ImageDraw.Draw(im)
    draw.text((200, 200), s, font=font, fill = 255)
    glow = im.filter(ImageFilter.GaussianBlur(10))
    im = ImageChops.add(im, glow)
    return im.crop(im.getbbox())

def preview(cmdbuf):
    print('preview is', len(cmdbuf), 'bytes')
    from gameduino_spidriver import GameduinoSPIDriver
    gd = GameduinoSPIDriver()
    gd.init()
    gd.cc(cmdbuf)
    gd.finish()
    
class Gameduino(_EVE, EVE):
    def __init__(self):
        self.buf = b''

    def cc(self, s):
        assert (len(s) % 4) == 0
        self.buf += s

    def pack(self):
        print(len(self.buf), "bytes used")
        while len(self.buf) < (4096 - 4):
            self.cmd_dlstart()
        self.cc(struct.pack("I", 0x7c6a0100))
        assert len(self.buf) == 4096

    def flush(self):
        pass

    def finish(self):
        pass

    def video_signal(self, h_Active, h_Front, h_Sync, h_Back, h_Total, v_Active, v_Front, v_Sync, v_Back, v_Total):
        assert((h_Active + h_Front + h_Sync + h_Back) == h_Total)
        assert((v_Active + v_Front + v_Sync + v_Back) == v_Total)

        # self.cmd_regwrite(gd3.REG_ADAPTIVE_FRAMERATE, 0)

        self.cmd_regwrite(gd3.REG_HCYCLE, h_Total)
        self.cmd_regwrite(gd3.REG_HOFFSET, h_Sync + h_Back)
        self.cmd_regwrite(gd3.REG_HSIZE, h_Active)

        self.cmd_regwrite(gd3.REG_VCYCLE, v_Total)
        self.cmd_regwrite(gd3.REG_VOFFSET, v_Sync + v_Back)
        self.cmd_regwrite(gd3.REG_VSIZE, v_Active)

        # See CEA-861 p.21
        self.cmd_regwrite(gd3.REG_HSYNC1, 0)
        self.cmd_regwrite(gd3.REG_HSYNC0, h_Sync)

        self.cmd_regwrite(gd3.REG_VSYNC1, 0)
        self.cmd_regwrite(gd3.REG_VSYNC0, v_Sync)

        if 0:
            self.cmd_regwrite(gd3.REG_TRIM, 23)
            self.cmd_regwrite(0x302614, 0x8c1)

        self.cmd_regwrite(gd3.REG_PCLK, 1)
    def setup_1280x720(self):
        if 1:

            self.Clear()
            self.swap()
            setup = [
                # (gd3.REG_OUTBITS, 0),
                (gd3.REG_DITHER, 0),
                (gd3.REG_GPIO, 0x83),
                (gd3.REG_CSPREAD, 0),
                (gd3.REG_PCLK_POL, 0),
                (gd3.REG_ADAPTIVE_FRAMERATE, 0),
            ]
            for (a, v) in setup:
                self.cmd_regwrite(a, v)

            self.video_signal(
                h_Active = 1280,
                h_Front = 110,
                h_Sync = 40,
                h_Back = 220,
                h_Total = 1650,
                v_Active = 720,
                v_Front = 5,
                v_Sync = 5,
                v_Back = 20,
                v_Total = 750)
            self.w = 1280
            self.h = 720
            return

def make_bringup():
    gd = Gameduino()
    gd.setup_1280x720()

    blob_addr = 0x8000
    gd.cmd_inflate(blob_addr)
    img = open("unified.blob", "rb").read()
    c = align4(zlib.compress(img))
    gd.cc(c)
    gd.cmd_flashupdate(0, blob_addr, 4096)
    gd.cmd_flashfast()

    if 1:
        gd.VertexFormat(0)
        gd.ClearColorRGB(0xff, 0xff, 0xff)
        gd.SaveContext()
        gd.Clear()
        gd.ClearColorRGB(0, 0, 0)
        gd.ScissorSize(1280 - 2, 720 - 2)
        gd.ScissorXY(1, 1)
        gd.Clear()

        (x0, x1) = (20, 1280 - 20)
        (y, H, Y) = (20, 50, 120)
        for i,(cname, rgb) in enumerate([("red", 0xff0000), ("green", 0xff00), ("blue", 0xff), ("white", 0xffffff)]):
            gd.ScissorSize(x1 - x0, H)
            gd.ScissorXY(x0, y)
            gd.cmd_gradient(x0, 0, 0x000000, x1, 0, rgb)
            y += Y
        gd.RestoreContext()

        gd.cmd_setbitmap(0, gd3.RGB332, 1, 1)
        gd.BitmapSize(gd3.NEAREST, gd3.REPEAT, gd3.REPEAT, 40, 40)

        def part(i, name):
            x = 200 + 300 * (i // 2)
            y = 500 + 70 * (i % 2)
            gd.cmd_text(x, y, 31, 0, name + "")
            gd.Cell(i)
            gd.Vertex2f(x + 220, y + 5)
        tests = ["flash  U2", "flash  U4", "    AUDIO"]
        [part(i, n) for (i, n) in enumerate(tests)]
        gd.cmd_memset(0, 0b01001001, len(tests)) # all gray initially

        gd.cmd_text(640, 690, 31, gd3.OPT_CENTER, __VERSION__)
        gd.swap()

    print('bringup is', len(gd.buf), 'bytes')
    tb = " ".join([("%d c," % b) for b in gd.buf])
    with open("_bringup.fs", "wt") as f:
        f.write(textwrap.fill(tb, 127))
    return gd.buf

def poweron():
    gd = Gameduino()
    gd.setup_1280x720()

    gd.BitmapHandle(0)
    gd.cmd_loadimage(0, 0)
    (w, h) = Image.open("gameduino.png").size
    gd.cc(align4(open("gameduino.png", "rb").read()))
    gd.BitmapSize(gd3.NEAREST, gd3.BORDER, gd3.BORDER, 0, 0)

    H = 0x60
    grid = Image.frombytes("L", (4, 4), bytes([
        H, H, H, H,
        H, 0, 0, 0,
        H, 0, 0, 0,
        H, 0, 0, 0]))
    buf = BytesIO()
    grid.save(buf, "PNG")
    gd.BitmapHandle(1)
    gd.cmd_loadimage(-1, 0)
    gd.cc(align4(buf.getvalue()))
    gd.BitmapSize(gd3.BILINEAR, gd3.REPEAT, gd3.REPEAT, 0, 0)

    daz = gentext("dazzler")
    buf = BytesIO()
    daz.save(buf, "PNG")
    gd.BitmapHandle(2)
    gd.cmd_loadimage(-1, 0)
    gd.cc(align4(buf.getvalue()))

    gd.ClearColorRGB(0x20, 0x00, 0x00)
    gd.Clear()
    gd.Begin(gd3.BITMAPS)

    gd.SaveContext()
    gd.cmd_scale(3, 3)
    gd.cmd_setmatrix()
    gd.BitmapHandle(0)
    gd.Vertex2f((1280 - 3*w) / 2, 65)
    gd.RestoreContext()

    gd.SaveContext()
    gd.cmd_loadidentity()
    gd.cmd_scale(0.75, 0.75)
    gd.cmd_setmatrix()
    gd.ColorRGB(0x20, 0x00, 0x00)

    gd.BitmapHandle(1)
    gd.Vertex2f(0, 0)
    gd.RestoreContext()

    gd.BitmapHandle(2)
    gd.ColorA(0xf0)
    (x, y) = ((1280 - daz.size[0]) / 2, 380)
    gd.Vertex2f(x, y)

    gd.cmd_text(640, 690, 31, gd3.OPT_CENTER, __VERSION__)

    gd.swap()
    print('poweron is', len(gd.buf), 'bytes')
    return gd.buf

def make_textmode():
    font = ImageFont.truetype("../../.fonts/IBMPlexMono-Text.otf", 21)
    ch = [chr(i) for i in range(32, 127)]

    im = Image.new("L", (256, 256))
    draw = ImageDraw.Draw(im)
    for c in ch:
        draw.text((128, 128), c, font=font, fill=255)
    (x0, y0, _, _) = im.getbbox()
    print(128 - x0, 128 - y0)
    im = im.crop(im.getbbox())
    print(im)
    im.save("out.png")

    (w, h) = im.size
    im = Image.new("L", (w, h))
    draw = ImageDraw.Draw(im)
    for c in ch:
        draw.text((128 - x0, 128 - y0), c, font=font, fill=255)
    im = im.crop(im.getbbox())
    print(im)
    im.save("out.png")

    fim = Image.new("L", (w, h * 96))
    draw = ImageDraw.Draw(fim)
    for i,c in enumerate(ch):
        draw.text((128 - x0, (128 - y0) + (h * i)), c, font=font, fill=255)

    gd = Gameduino()

    def size(a, b):
        gd.BitmapSize(gd3.NEAREST, gd3.BORDER, gd3.BORDER, a, b)
        gd.BitmapSizeH(a >> 9, b >> 9)

    gd.cmd_inflate(0)
    c = align4(zlib.compress(fim.tobytes()))
    gd.cc(c)

    w2 = w + 2
    h2 = h * 28 // 22
    (W, H) = (1280 // w2, (720 // h2) + 1)
    ht = H * h2
    y_bar = (720 - (H - 1) * h2) // 2
    x_bar = (1280 - (W * w2)) // 2

    print('font size', (w, h), (w2, h2), 'screen size', (W, H - 1))
    print('font bytes', len(fim.tobytes()))
    print('bars:', (x_bar, y_bar))
    print(w * W * h2 * H)

    gd.BitmapHandle(0)
    fb = 0x10000
    gd.cmd_setbitmap(fb, gd3.L8, w, ht)
    gd.cmd_memset(fb, 0x00, W * w * ht)

    gd.BitmapHandle(1)
    cm = 0x8000
    gd.cmd_setbitmap(cm, gd3.RGB565, 1, H)
    size(w2, ht)
    b = bytes([rr(256) for i in range(2 * 2 * W * H)])
    gd.cmd_memwrite(cm, len(b))
    gd.cc(align4(b))

    def gaddr(x, y):
        return fb + y * (w * h2) + (x * w * ht)
    def caddr(x, y, z):
        return cm + 2 * ((y + H * x) + z * (W * H))
    def drawch(x, y, c, color = 0xffff, bg = 0x0000):
        dst = gaddr(x, y)
        src = (ord(c) - 0x20) * (w * h)
        gd.cmd_memcpy(dst, src, (w * h))
        # gd.cmd_memset(dst, 0xff, (w * h))

        gd.cmd_memwrite(caddr(x, y, 0), 2)
        gd.cc(struct.pack("<I", color))
        gd.cmd_memwrite(caddr(x, y, 1), 2)
        gd.cc(struct.pack("<I", bg))

    gd.setup_1280x720()

    offset = 1
    vh = y_bar + ((H - offset) * h2)

    def drawtwice(x):
        gd.Macro(0)
        if x:
            yo = 0
        else:
            yo = (h2 - h) // 2
        for i in range(1280 // w2):
            gd.Cell(i)
            gd.Vertex2f(x_bar + x + w2 * i, -ht + yo)
            gd.Vertex2f(x_bar + x + w2 * i, 0 + yo)

    def color_panel(z):
        gd.SaveContext()
        gd.BitmapHandle(1)
        gd.BitmapSource(caddr(0, 0, z))
        gd.BitmapTransformA(0, 1)
        gd.BitmapTransformE(32768 // h2 + 1, 1)
        drawtwice(-1)
        gd.RestoreContext()

    gd.cmd_memwrite(gd3.REG_MACRO_0, 4)
    gd.VertexTranslateY(vh << 4)

    gd.VertexFormat(0)
    gd.ClearColorA(0)
    # gd.ClearColorRGB(200, 200, 200)
    gd.Clear()
    gd.ScissorXY(x_bar, y_bar)
    gd.ScissorSize((W * w2), (H - 1) * h2)
    gd.Begin(gd3.BITMAPS)

    gd.ColorMask(1, 1, 1, 0)
    color_panel(1)

    gd.ColorMask(0, 0, 0, 1)
    gd.BlendFunc(1, 0)
    gd.BitmapHandle(0)
    drawtwice(0)

    gd.ColorMask(1, 1, 1, 0)
    gd.BlendFunc(gd3.DST_ALPHA, gd3.ONE_MINUS_DST_ALPHA)
    color_panel(0)

    gd.swap()

    for i in range(H):
        s = "[{0}]".format(i)
        for j,c in enumerate(s):
            drawch(i + j, i, c, 0xffff, 0x1010)

    return gd.buf

def make_bootstream(poweron_stream):
    gd = Gameduino()
    gd.setup_1280x720()

    if 0:
        gd.cmd_loadimage(0, 0)
        (w, h) = Image.open("gameduino.png").size
        gd.cc(align4(open("gameduino.png", "rb").read()))
        gd.ClearColorRGB(0x20, 0x00, 0x00)
        gd.Clear()
        gd.Begin(gd3.BITMAPS)
        gd.Vertex2ii((1280 - w) // 2, (720 - h) // 2)
        gd.swap()

    if 1:
        gd.ClearColorRGB(0xff, 0xff, 0xff)
        gd.SaveContext()
        gd.Clear()
        gd.ClearColorRGB(0, 0, 0)
        gd.ScissorSize(1280 - 2, 720 - 2)
        gd.ScissorXY(1, 1)
        gd.Clear()

        (x0, x1) = (20, 1280 - 20)
        (y, H, Y) = (20, 80, 120)
        for i,(cname, rgb) in enumerate([("red", 0xff0000), ("green", 0xff00), ("blue", 0xff), ("white", 0xffffff)]):
            gd.ScissorSize(x1 - x0, H)
            gd.ScissorXY(x0, y)
            gd.cmd_gradient(x0, 0, 0x000000, x1, 0, rgb)
            y += Y
        gd.RestoreContext()

        gd.swap()

        fl = open("dazzler.bit", "rb").read()[96:]
        fl = fl.ljust(512 * 1024, b'\xff')
        fl += struct.pack("HH", 0x947a, len(poweron_stream)) + poweron_stream
        with open("_loadflash.fs", "wt") as h:
            h.write("manufacturer hex\n")
            h.write(": m >spi ;\n")
            # r ( u n ) write u n times
            h.write(": r 0 do dup >spi loop drop ;\n")
            def addr(a):
                return "%x m %x m %x m " % (0xff & (a >> 16), 0xff & (a >> 8), 0xff & a)
            fl = fl[:]
            for i in range(0, len(fl), 4096):
                h.write("20 wcmd " + addr(i) + "notbusy \ %#x\n" % i)
                pg = fl[i:i+4096]
                for j in range(0, len(pg), 256):
                    s = pg[j:j+256]
                    if set(s) != {0xff}:
                        h.write("02 wcmd " + addr(i + j) + "\ %#x \n" % (i + j))
                        if 1:
                            l = []
                            while s:
                                (v, n) = [(k,len(list(v))) for (k,v) in groupby(s,int)][0]
                                if n > 1:
                                    s = s[n:]
                                    l.append("%x %x r" % (v, n))
                                else:
                                    c = s[0]
                                    s = s[1:]
                                    l.append("%x m" % c)
                            l.append("notbusy")
                            h.write(textwrap.fill(" ".join(l), 126) + "\n")
                        else:
                            h.write(textwrap.fill(" ".join(["%x m" % c for c in s]), 127))
                            h.write("\nnotbusy\n")
            print(len(fl))
            s = sum(fl[:]) & 0xffff
            print("Expected checksum %04x" % s)
            with open("flash.bin", "wb") as f:
                f.write(fl)
            checkline = "$%x. fl.check \ expect %x\n" % (len(fl), s)
            print(checkline)
            h.write(checkline)
            h.write("decimal\n")

            if 0:
                with open("dump.hex", "wt") as f:
                    for i in range(0x26000, 0x28000, 16):
                        f.write("%04X  " % (i & 0xffff))
                        for j in range(16):
                            c = fl[i + j]
                            f.write("%02X " % c)
                        f.write("\n")

if __name__ == "__main__":
    br = make_bringup()
    po = poweron()
    te = make_textmode()
    preview(te)
    # make_bootstream(po)
