import textwrap
import struct
import array
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import bteve as eve
import zlib
from io import BytesIO
from itertools import groupby
from gameduino2.convert import convert
import random
import binascii
def crc(s):     # CRC-32 of string s
    return binascii.crc32(s) & 0xffffffff
import common

random.seed(7)
rr = random.randrange

__VERSION__ = "1.0.4"

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
    
class Gameduino(eve.Gameduino):
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

        # self.cmd_regwrite(eve.REG_ADAPTIVE_FRAMERATE, 0)

        self.cmd_regwrite(eve.REG_HCYCLE, h_Total)
        self.cmd_regwrite(eve.REG_HOFFSET, h_Sync + h_Back)
        self.cmd_regwrite(eve.REG_HSIZE, h_Active)

        self.cmd_regwrite(eve.REG_VCYCLE, v_Total)
        self.cmd_regwrite(eve.REG_VOFFSET, v_Sync + v_Back)
        self.cmd_regwrite(eve.REG_VSIZE, v_Active)

        # See CEA-861 p.21
        self.cmd_regwrite(eve.REG_HSYNC1, 0)
        self.cmd_regwrite(eve.REG_HSYNC0, h_Sync)

        self.cmd_regwrite(eve.REG_VSYNC1, 0)
        self.cmd_regwrite(eve.REG_VSYNC0, v_Sync)

        if 0:
            self.cmd_regwrite(eve.REG_TRIM, 23)
            self.cmd_regwrite(0x302614, 0x8c1)

        self.cmd_regwrite(eve.REG_PCLK, 1)
    def setup_1280x720(self):
        if 1:

            self.Clear()
            self.swap()
            setup = [
                (eve.REG_OUTBITS, 0),
                (eve.REG_DITHER, 0),
                (eve.REG_GPIO, 0x83),
                (eve.REG_CSPREAD, 0),
                (eve.REG_PCLK_POL, 0),
                (eve.REG_ADAPTIVE_FRAMERATE, 0),
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

    def setup_640_480(self):
        if 1:

            self.Clear()
            self.swap()
            setup = [
                # (eve.REG_OUTBITS, 0),
                (eve.REG_DITHER, 0),
                (eve.REG_GPIO, 0x83),
                (eve.REG_CSPREAD, 0),
                (eve.REG_PCLK_POL, 0),
                (eve.REG_ADAPTIVE_FRAMERATE, 0),

                (eve.REG_HCYCLE, 800),
                (eve.REG_HOFFSET, 16 + 96),
                (eve.REG_HSIZE, 640),

                (eve.REG_HSYNC1, 0),
                (eve.REG_HSYNC0, 96),

                (eve.REG_VCYCLE, 525),
                (eve.REG_VOFFSET, 12),
                (eve.REG_VSIZE, 480),

                (eve.REG_VSYNC1, 0),
                (eve.REG_VSYNC0, 10),
            ]
            for (a, v) in setup:
                self.cmd_regwrite(a, v)

        if 0:
            self.cmd_regwrite(eve.REG_TRIM, 23)
            self.cmd_regwrite(0x302614, 0x8c1)

        self.cmd_regwrite(eve.REG_PCLK, 3)
        self.w = 640
        self.h = 480

def make_fallback():
    gd = Gameduino()
    # gd.setup_640_480()
    gd.setup_1280x720()

    gd.ClearColorRGB(0, 40, 0)
    gd.Clear()
    gd.cmd_text(100, 100, 31, 0, "FALLBACK")
    gd.swap()

    return gd.buf

def sector_1():
    gd = Gameduino()
    gd.setup_1280x720()
    gd.pack()
    return gd.buf

def make_flash():
    gd = Gameduino()
    blob_addr = 0x8000
    gd.cmd_inflate(blob_addr)
    img = open("unified.blob", "rb").read() + sector_1()
    assert len(img) == 8192
    c = eve.align4(zlib.compress(img, 9))
    gd.cc(c)
    gd.cmd_flashupdate(0, blob_addr, len(img))
    gd.cmd_flashfast()
    return gd.buf

def make_bringup():
    gd = Gameduino()
    gd.setup_1280x720()

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

        gd.cmd_setbitmap(0, eve.RGB332, 1, 1)
        gd.BitmapSize(eve.NEAREST, eve.REPEAT, eve.REPEAT, 40, 40)

        def part(i, name):
            x = 200 + 300 * (i // 3)
            y = 470 + 60 * (i % 3)
            gd.cmd_text(x + 190, y, 31, eve.OPT_RIGHTX, name + "")
            gd.Cell(i)
            gd.Vertex2f(x + 220, y + 5)
        tests = ["flash U2",
                 "flash U4",
                 "U4 quad",
                 "EVE audio",
                 "EVE quad",
                 "video bus",
                 "i2c",
                 "clock",
                 "Loaded" ]
        [part(i, n) for (i, n) in enumerate(tests)]
        gd.cmd_memset(0, 0b01001001, len(tests)) # all gray initially

        gd.cmd_text(640, 690, 31, eve.OPT_CENTER, __VERSION__)

        if 0:
            gd.Cell(0)
            gd.cmd_setbitmap(0x1000, eve.RGB565, 512, 400)
            gd.Vertex2f(5, 5)

        gd.ColorRGB(0xe0, 0xe0, 0xe0)
        gd.cmd_text(10, 690, 29, eve.OPT_CENTERY | eve.OPT_FORMAT, "%s", 0xb0000)
        gd.cmd_text(1270, 690, 29, eve.OPT_RIGHTX | eve.OPT_CENTERY | eve.OPT_FORMAT, "%s", 0xb0100)

        gd.swap()

    return gd.buf

def poweron():
    gd = Gameduino()
    gd.setup_1280x720()

    # Make sure $c0000 is 0x15
    gd.cmd_memwrite(0xc0000, 1)
    gd.cc(b'\x15' * 4)

    ld = common.Loader(gd)
    ld.add = ld.uadd

    # Handle 0: gameduino logo
    gd.BitmapHandle(0)
    im = Image.open("gameduino.png").convert("RGB")
    ld.RGB565(im)
    (w, h) = im.size
    gd.BitmapSize(eve.NEAREST, eve.BORDER, eve.BORDER, 0, 3 * h)

    # Handle 1: grid
    H = 0x60
    grid = Image.frombytes("L", (4, 4), bytes([
        H, H, H, H,
        H, 0, 0, 0,
        H, 0, 0, 0,
        H, 0, 0, 0]))
    gd.BitmapHandle(1)
    ld.L8(grid)
    gd.BitmapSize(eve.BILINEAR, eve.REPEAT, eve.REPEAT, 0, 3 * h)

    # Handle 2: dazzler glowing text
    daz = gentext("dazzler")
    gd.BitmapHandle(2)
    ld.L8(daz)


    gd.ClearColorRGB(0x20, 0x00, 0x00)
    gd.Clear()
    gd.Begin(eve.BITMAPS)

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

    gd.cmd_text(640, 690, 31, eve.OPT_CENTER, __VERSION__)
    gd.ColorRGB(0xe0, 0xe0, 0xe0)
    gd.cmd_text(10, 690, 29, eve.OPT_CENTERY | eve.OPT_FORMAT, "%s", 0xb0000)
    gd.cmd_text(1270, 690, 29, eve.OPT_RIGHTX | eve.OPT_CENTERY | eve.OPT_FORMAT, "%s", 0xb0100)

    gd.swap()
    print('poweron is', len(gd.buf), 'bytes')
    return gd.buf

def make_textmode():
    font = ImageFont.truetype("../../.fonts/IBMPlexMono-SemiBold.otf", 13)
    ch = [chr(i) for i in range(32, 255)]

    im = Image.new("L", (256, 256))
    draw = ImageDraw.Draw(im)
    for c in ch:
        draw.text((128, 128), c, font=font, fill=255)
    (x0, y0, _, _) = im.getbbox()
    print(128 - x0, 128 - y0)
    im = im.crop(im.getbbox())
    # im.save("out.png")

    (w, h) = im.size

    fim = Image.new("L", (w, h * len(ch)))
    draw = ImageDraw.Draw(fim)
    for i,c in enumerate(ch):
        draw.text((128 - x0, (128 - y0) + (h * i)), c, font=font, fill=255)
    # fim.save("out.png")

    gd = Gameduino()

    def size(a, b):
        gd.BitmapSize(eve.NEAREST, eve.BORDER, eve.BORDER, a, b)
        gd.BitmapSizeH(a >> 9, b >> 9)

    (sw, sh) = (720, 1280)
    w2 = w + 1
    h2 = h * 28 // 22
    (W, H) = (sw // w2, (sh // h2) + 1)
    ht = H * h2
    y_bar = (sh - (H - 1) * h2) // 2
    x_bar = (sw - (W * w2)) // 2

    gx = w * ht             # glyph x term
    gy = w * h2             # glyph y term
    cx = 2 * H              # color x term
    cz = 2 * H * W          # color z term
    wh = w * h
    sz = w * W * h2 * H

    cm = 0
    fm = cm + 2 * cz
    fb = fm + len(fim.tobytes())

    gd.Clear()
    gd.swap()

    gd.cmd_inflate(fm)
    c = eve.align4(zlib.compress(fim.tobytes()))
    gd.cc(c)

    print('font size', (w, h), (w2, h2), 'screen size', (W, H - 1))
    print('font bytes', len(fim.tobytes()))
    print('bars:', (x_bar, y_bar))

    gd.BitmapHandle(0)
    gd.cmd_setbitmap(fb, eve.L8, w, ht)
    gd.cmd_memset(fb, 0x00, W * w * ht)

    gd.BitmapHandle(1)
    gd.cmd_setbitmap(cm, eve.RGB565, 1, H)
    size(w2, ht)
    if 0:
        b = bytes([rr(256) for i in range(2 * 2 * W * H)])
        gd.cmd_memwrite(cm, len(b))
        gd.cc(eve.align4(b))
    else:
        gd.cmd_memzero(cm, 2 * 2 * W * H)

    with open("_textmode.fs", "wt") as f:
        for v in ("fm", "fb", "cm", "sz"):
            f.write("$%x. 2constant %s\n" % (eval(v), v))
        for v in ("H", "W", "gx", "gy", "cx", "cz", "wh", "y_bar", "h2"):
            f.write("$%x constant %s\n" % (eval(v), v))

    def gaddr(x, y):
        return fb + w * ((y * h2) + (x * ht))
    def caddr(x, y, z):
        return cm + 2 * (y + H * (x + z * W))
    def drawch(x, y, c, color = 0xffff, bg = 0x0000):
        dst = gaddr(x, y)
        src = fm + (ord(c) - 0x20) * (w * h)
        gd.cmd_memcpy(dst, src, (w * h))
        # gd.cmd_memset(dst, 0xff, (w * h))

        gd.cmd_memwrite(caddr(x, y, 0), 2)
        gd.cc(struct.pack("<I", color))
        gd.cmd_memwrite(caddr(x, y, 1), 2)
        gd.cc(struct.pack("<I", bg))

    gd.setup_1280x720()
    gd.cmd_setrotate(2)

    offset = 0
    vh = y_bar + ((H - offset) * h2)

    def drawtwice(x):
        gd.Macro(0)
        if x:
            yo = 0
        else:
            yo = (h2 - h) // 2
        for i in range(sw // w2):
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

    gd.cmd_memwrite(eve.REG_MACRO_0, 4)
    gd.VertexTranslateY(vh << 4)

    gd.VertexFormat(0)
    gd.ClearColorA(0)
    # gd.ClearColorRGB(200, 200, 200)
    gd.Clear()
    gd.ScissorXY(x_bar, y_bar)
    gd.ScissorSize((W * w2), (H - 1) * h2)
    gd.Begin(eve.BITMAPS)

    gd.ColorMask(1, 1, 1, 0)
    color_panel(1)

    gd.ColorMask(0, 0, 0, 1)
    gd.BlendFunc(1, 0)
    gd.BitmapHandle(0)
    drawtwice(0)

    gd.ColorMask(1, 1, 1, 0)
    gd.BlendFunc(eve.DST_ALPHA, eve.ONE_MINUS_DST_ALPHA)
    color_panel(0)

    gd.swap()

    if 0:
        for i in range(H):
            s = "[{0}]".format(i)
            for j,c in enumerate(s):
                drawch(i + j, i, c, 0xffff, 0x1010)

    return gd.buf

def make_loadflash(fn, fl):
    print('%s: bitstream is %d bytes, compresses to %d bytes' % (fn, len(fl), len(zlib.compress(fl, 9))))
    assert len(fl) % 256 == 0, len(fl)
    LP = 0x1000 # load point
    gd = Gameduino()
    gd.cmd_inflate(LP)
    gd.cc(eve.align4(zlib.compress(fl)))
    gd.cmd_memcrc(0, len(fl), 0)
    ecrc = crc(fl)

    gd.cmd_memwrite(0xffff8, 8)
    gd.c4(len(fl))
    gd.c4(ecrc)
    gd.cmd_memcrc(LP, len(fl), 0)
    print('Expected CRC %x' % crc(fl))

    b = gd.buf
    padw = (-len(b) & 0xff) // 4
    b = (padw * struct.pack("I", 0xffffff5b)) + b
    with open(fn, "wb") as h:
        h.write(b)

    with open(fn.replace(".bin", ".h"), "wt") as f:
        for i in range(0, len(b), 100):
            f.write("".join(["%d," % x for x in b[i:i + 100]]) + "\n")

    return

    with open(fn, "wt") as h:
        h.write("0 MUX0 CSPI stream : m >spid ; hex\n")
        db = array.array("I", gd.buf)
        l = []
        for x in db:
            l += ["%x." % x, "m"]
        l += ["result .x .x"]
        h.write(textwrap.fill(" ".join(l), 127) + "\n")
        h.write("( expect %08X )\n" % ecrc)

        s = sum(fl[:]) & 0xffff
        print("Expected checksum %04x" % s)
        h.write("$%x. e2fl\n" % (len(fl)))
        h.write("$%x. fl.check \ expect %x\n" % (len(fl), s))
        h.write("decimal\n")

def make_bootstream(streams):
    gd = Gameduino()
    gd.setup_1280x720()

    if 0:
        gd.cmd_loadimage(0, 0)
        (w, h) = Image.open("gameduino.png").size
        gd.cc(eve.align4(open("gameduino.png", "rb").read()))
        gd.ClearColorRGB(0x20, 0x00, 0x00)
        gd.Clear()
        gd.Begin(eve.BITMAPS)
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

        desync = bytes([int(w, 16) for w in "30 a1 00 0d".split()])
        p = fl.index(desync)
        set_general5 = bytes([int(w, 16) for w in "32 e1 da 22".split()])
        fl_loader = fl[:p] + set_general5 + fl[p:]

        with open("_jtagboot.h", "wt") as f:
            for i in range(0, len(fl_loader), 100):
                f.write("".join(["%d,"%b for b in fl_loader[i:i + 100]]) + "\n")

        fl = fl.ljust(0x54000, b'\xff')
        make_loadflash("_loadflash_min.bin", fl)

        def autoexec(cmd):
            return (fl + cmd).ljust(0x54100, b'\xff')
        make_loadflash("_loadflash_dev.bin", autoexec(b'." DEV BUILD AUTOEXEC "'))

        def cust():
            f = autoexec(b'poweron')
            f = f.ljust(512 * 1024, b'\xff')
            f += struct.pack("H", 0x947a)
            for s in streams:
                f += struct.pack("I", len(s)) + s
            f += b'\xff' * (-len(f) & 0xff)
            return f
        make_loadflash("_loadflash_cust.bin", cust())

        if 1:
            fl = fl.ljust(512 * 1024, b'\xff')
            fl += struct.pack("H", 0x947a)
            for s in streams:
                fl += struct.pack("I", len(s)) + s

        gd = Gameduino()
        gd.cmd_inflate(0x1000)
        gd.cc(eve.align4(zlib.compress(fl)))
        ecrc = crc(fl)

        gd.cmd_memwrite(0xffff8, 8)
        gd.c4(len(fl))
        gd.c4(ecrc)
        gd.cmd_memcrc(0x1000, len(fl), 0)
        print('Expected CRC %x' % ecrc)

        with open("_loadflash2.fs", "wt") as h:
            h.write("0 MUX0 CSPI stream : m >spid ; hex\n")
            db = array.array("I", gd.buf)
            l = []
            for x in db:
                l += ["%x." % x, "m"]
            l += ["result .x .x"]
            h.write(textwrap.fill(" ".join(l), 127) + "\n")
            h.write("( expect %08X )\n" % ecrc)

            s = sum(fl[:]) & 0xffff
            print("Expected checksum %04x" % s)
            h.write("$%x. e2fl\n" % (len(fl)))
            h.write("$%x. fl.check \ expect %x\n" % (len(fl), s))
            h.write("decimal\n")

        b = gd.buf
        padw = (-len(b) & 0xff) // 4
        b = (padw * struct.pack("I", 0xffffff5b)) + b

        with open("_loadflash2.bin", "wb") as h:
            h.write(b)

        with open("_loadflash2.h", "wt") as f:
            for i in range(0, len(b), 100):
                f.write("".join(["%d,"%x for x in b[i:i + 100]]) + "\n")

        return

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

def dump_include(filename, bb, op = ">spi"):
    tb = " ".join([("%d %s" % (b, op)) for b in bb])
    with open(filename, "wt") as f:
        f.write("eve-start stream\n")
        f.write(textwrap.fill(tb, 127))
        f.write("\nfinish\n")

def dump_init(filename, bb):
    print(filename, "is", len(bb) // 4)
    lc = len(bb) // 4
    tb = " ".join([("%d %s" % (b, "c,")) for b in [lc] + list(bb)])
    with open(filename, "wt") as f:
        f.write(textwrap.fill(tb, 127))
        f.write("\n")

def make_sector_1():
    gd = Gameduino()
    gd.setup_1280x720()
    gd.pack()
    print("Sector 1 CRC %08X" % crc(gd.buf))
    cd = eve.align4(zlib.compress(gd.buf, 9))
    with open("_sector1.h", "wt") as f:
        f.write(",".join([str(s) for s in cd]))
        f.write("\n")

if __name__ == "__main__":
    make_sector_1()

    br = make_bringup()
    dump_init("_bringup.fs", br)

    fl = make_flash()
    dump_init("_flash.fs", fl)

    po = poweron()
    te = make_textmode()
    fa = make_fallback()
    # preview(fa)
    dump_include("_fallback.fs", fa)
    # preview(te)
    # make_bootstream([po, te]) # xxx does not fit on teensy?!
    make_bootstream([po])
