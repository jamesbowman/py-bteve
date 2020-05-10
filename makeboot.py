import textwrap
import struct
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from _eve import _EVE
from eve import EVE, align4
import registers as gd3
import zlib
from io import BytesIO
from itertools import groupby

__VERSION__ = "0.0.2"

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

def trial(cmdbuf):
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

    gd.cmd_inflate(0)
    img = open("unified.blob", "rb").read()
    c = align4(zlib.compress(img))
    gd.cc(c)
    gd.cmd_flashupdate(0, 0, 8192)
    gd.cmd_flashfast()

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

        gd.cmd_text(640, 690, 31, gd3.OPT_CENTER, __VERSION__)
        gd.swap()

    print('bringup is', len(gd.buf), 'bytes')
    tb = " ".join([("%d c," % b) for b in gd.buf])
    with open("_bringup.fs", "wt") as f:
        f.write(textwrap.fill(tb, 127))

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
            h.write(": m >spi ; hex\n")
            # r ( u n ) write u n times
            h.write(": r 0 do dup >spi loop drop ;\n")
            def addr(a):
                return "%x m %x m %x m " % (0xff & (a >> 16), 0xff & (a >> 8), 0xff & a)
            for i in range(0, len(fl), 4096):
                h.write("$20 wcmd " + addr(i) + "notbusy \ %d\n" % (i / 1000))
                pg = fl[i:i+4096]
                for j in range(0, len(pg), 256):
                    s = pg[j:j+256]
                    if set(s) != {0xff}:
                        h.write("$02 wcmd " + addr(i + j) + "\n")
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
                            h.write(textwrap.fill(" ".join(l), 127) + "\n")
                        else:
                            h.write(textwrap.fill(" ".join(["%x m" % c for c in s]), 127))
                            h.write("\nnotbusy\n")
            print(len(fl))
            s = sum(fl[:]) & 0xffff
            print("Expected checksum %04x" % s)
            h.write("%x. fl.check \ expect %x\n" % (len(fl), s))
            h.write("decimal\n")

if __name__ == "__main__":
    make_bringup()
    po = poweron()
    trial(po)
    make_bootstream(po)
