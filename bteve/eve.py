import struct
import array
from collections import namedtuple

from .registers import *

_B0 = b'\x00'
def align4(s):
    """
    :param bytes s: input bytes object
    :return: the bytes object extended so that its length is a multiple of 4
    """
    return s + _B0 * (-len(s) & 3)

def f16(v):
    return int(round(65536 * v))

def furmans(deg):
    """ Given an angle in degrees, return it in Furmans """
    return 0xffff & f16(deg / 360.0)

# Order matches the register layout, so can fill with a single block read
_Touch = namedtuple(
    "TouchInputs",
    (
    "rawy",
    "rawx",
    "rz",
    "y",
    "x",
    "tag_y",
    "tag_x",
    "tag",
    ))
_State = namedtuple(
    "State",
    (
    "touching",
    "press",
    "release"
    ))
_Tracker = namedtuple(
    "Tracker",
    (
    "tag",
    "val"
    ))
_Inputs = namedtuple(
    "Inputs",
    (
    "touch",
    "tracker",
    "state",
    ))

class EVE:

    def cstring(self, s):
        if type(s) == str:
            s = bytes(s, "utf-8")
        self.cc(align4(s + _B0))

    def fstring(self, aa):
        self.cstring(aa[0])
        # XXX MicroPython is currently lacking array.array.tobytes()
        self.cc(bytes(array.array("i", aa[1:])))

    def cmd_append(self, *args):
        self.cmd(0x1e, "II", args)

    def cmd_bgcolor(self, *args):
        self.cmd(0x09, "I", args)

    def cmd_bitmap_transform(self, *args):
        self.cmd(0x21, "iiiiiiiiiiiiI", args)

    def cmd_touch_transform(self, *args):
        self.cmd(0x20, "iiiiiiiiiiiiI", args)

    def cmd_button(self, *args):
        self.cmd(0x0d, "hhhhhH", args[:6])
        self.fstring(args[6:])

    def cmd_calibrate(self, *args):
        self.cmd(0x15, "I", args)

    def cmd_clock(self, *args):
        self.cmd(0x14, "hhhHHHHH", args)

    def cmd_coldstart(self):
        self.cmd0(0x32)

    def cmd_dial(self, x, y, r, options, val):
        self.cmd(0x2d, "hhhHI", (x, y, r, options, furmans(val)))

    def cmd_dlstart(self):
        self.cmd0(0x00)

    def cmd_fgcolor(self, *args):
        self.cmd(0x0a, "I", args)

    def cmd_gauge(self, *args):
        self.cmd(0x13, "hhhHHHHH", args)

    def cmd_getmatrix(self, *args):
        self.cmd(0x33, "iiiiii", args)

    def cmd_getprops(self, *args):
        self.cmd(0x25, "III", args)

    def cmd_getptr(self, *args):
        self.cmd(0x23, "I", args)

    def cmd_gradcolor(self, *args):
        self.cmd(0x34, "I", args)

    def cmd_gradient(self, *args):
        self.cmd(0x0b, "hhIhhI", args)

    def cmd_inflate(self, *args):
        self.cmd(0x22, "I", args)

    def cmd_interrupt(self, *args):
        self.cmd(0x02, "I", args)

    def cmd_keys(self, *args):
        self.cmd(0x0e, "hhhhhH", args[:6])
        self.cstring(args[6])

    def cmd_loadidentity(self):
        self.cmd0(0x26)

    def cmd_loadimage(self, *args):
        self.cmd(0x24, "iI", args)

    def cmd_logo(self):
        self.cmd0(0x31)

    def cmd_memcpy(self, *args):
        self.cmd(0x1d, "III", args)

    def cmd_memcrc(self, *args):
        self.cmd(0x18, "III", args)

    def cmd_memset(self, *args):
        self.cmd(0x1b, "III", args)

    def cmd_memwrite(self, *args):
        self.cmd(0x1a, "II", args)

    def cmd_regwrite(self, ptr, val):
        self.cmd(0x1a, "III", (ptr, 4, val))

    def cmd_memzero(self, *args):
        self.cmd(0x1c, "II", args)

    def cmd_number(self, *args):
        self.cmd(0x2e, "hhhHi", args)

    def cmd_progress(self, *args):
        self.cmd(0x0f, "hhhhHHI", args)

    def cmd_regread(self, *args):
        self.cmd(0x19, "II", args)

    def cmd_rotate(self, a):
        self.cmd(0x29, "i", (furmans(a), ))

    def cmd_scale(self, sx, sy):
        self.cmd(0x28, "ii", (f16(sx), f16(sy)))

    def cmd_screensaver(self):
        self.cmd0(0x2f)

    def cmd_scrollbar(self, *args):
        self.cmd(0x11, "hhhhHHHH", args)

    def cmd_setfont(self, *args):
        self.cmd(0x2b, "II", args)

    def cmd_setmatrix(self):
        self.cmd0(0x2a)

    def cmd_sketch(self, *args):
        self.cmd(0x30, "hhHHII", args)

    def cmd_slider(self, *args):
        self.cmd(0x10, "hhhhHHI", args)

    def cmd_snapshot2(self, *args):
        self.cmd(0x37, "IIhhhh", args)

    def cmd_snapshot(self, *args):
        self.cmd(0x1f, "I", args)

    def cmd_spinner(self, *args):
        self.cmd(0x16, "hhHH", args)

    def cmd_stop(self):
        self.cmd0(0x17)

    def cmd_swap(self):
        self.cmd0(0x01)

    def cmd_text(self, *args):
        self.cmd(0x0c, "hhhH", args[0:4])
        self.fstring(args[4:])

    def cmd_toggle(self, *args):
        self.cmd(0x12, "hhhhHH", args[0:6])
        label = (args[6].encode() + b'\xff' + args[7].encode())
        self.fstring((label,) + args[8:])

    def cmd_touch_transform(self, *args):
        self.cmd(0x20, "iiiiiiiiiiiiI", args)

    def cmd_track(self, *args):
        self.cmd(0x2c, "hhhhi", args)

    def cmd_translate(self, tx, ty):
        self.cmd(0x27, "ii", (f16(tx), f16(ty)))

    #
    # The new 810 commands
    #

    def cmd_romfont(self, *args):
        self.SaveContext()
        self.cmd(0x3f, "II", args)
        self.RestoreContext()

    def cmd_mediafifo(self, *args):
        self.cmd(0x39, "II", args)

    def cmd_sync(self):
        self.cmd0(0x42)

    def cmd_setrotate(self, *args):
        self.cmd(0x36, "I", args)

    def cmd_setbitmap(self, *args):
        self.cmd(0x43, "IHhi", args)

    def cmd_setfont2(self, *args):
        self.cmd(0x3b, "III", args)

    def cmd_videoframe(self, *args):
        self.cmd(0x41, "II", args)

    def cmd_videostart(self):
        self.cmd(0x40, "", ())

    def cmd_videostartf(self):
        self.cmd(0x5f, "", ())

    # def cmd_snapshot2(self, 

    def cmd_playvideo(self, *args):
        self.cmd(0x3a, "I", args)

    def cmd_setscratch(self, *args):
        self.cmd(0x3c, "I", args)

    #
    # 815 commands
    #

    def cmd_setbase(self, *args):
        self.cmd(0x38, "I", args)

    def cmd_rotatearound(self, x, y, a, s = 1):
        self.cmd(0x51, "iiii", (x, y, furmans(a), f16(s)))

    def cmd_flasherase(self):
        self.cmd0(0x44)

    def cmd_flashwrite(self, a, b):
        self.cmd(0x45, "II", (a, len(b)))
        self.cc(b)

    def cmd_flashupdate(self, *args):
        self.cmd(0x47, "III", args)

    def cmd_flashread(self, *args):
        self.cmd(0x46, "III", args)

    def cmd_flashdetach(self):
        self.cmd0(0x48)

    def cmd_flashattach(self):
        self.cmd0(0x49)

    def cmd_flashfast(self):
        self.cmd(0x4a, "I", (0xdeadbeef,))

    def cmd_flashspidesel(self):
        self.cmd0(0x4b)

    def cmd_flashspitx(self, b):
        self.cmd(0x4c, "I", (len(b),))
        self.cc(align4(b))

    def cmd_flashspirx(self, ptr, num):
        self.cmd(0x4d, "II", (ptr, num))

    def cmd_flashsource(self, *args):
        self.cmd(0x4e, "I", args)

    def cmd_inflate2(self, *args):
        self.cmd(0x50, "II", args)

    def cmd_fillwidth(self, *args):
        self.cmd(0x58, "I", args)

    def cmd_appendf(self, *args):
        self.cmd(0x59, "II", args)

    def cmd_animframe(self, *args):
        self.cmd(0x5a, "hhII", args)

    def cmd_nop(self):
        self.cmd0(0x5b)

    #
    # 817 commands
    #

    def cmd_testcard(self, *args):
        self.cmd0(0x61)

    def cmd_hsf(self, *args):
        self.cmd(0x62, "I", args)

    def cmd_apilevel(self, *args):
        self.cmd(0x63, "I", args)

    def cmd_apilevel(self, *args):
        self.cmd(0x63, "I", args)

    def cmd_getimage(self):
        self.cmd(0x64, "5I", (0, 0, 0, 0, 0))

    def cmd_wait(self, *args):
        self.cmd(0x65, "I", args)

    def cmd_return(self):
        self.cmd0(0x66)

    def cmd_calllist(self, *args):
        self.cmd(0x67, "I", args)

    def cmd_newlist(self, *args):
        self.cmd(0x68, "I", args)

    def cmd_endlist(self):
        self.cmd0(0x69)

    # Some higher-level functions

    def get_inputs(self):
        self.finish()
        t = _Touch(*struct.unpack("HHIhhhhB", self.rd(REG_TOUCH_RAW_XY, 17)))

        r = _Tracker(*struct.unpack("HH", self.rd(REG_TRACKER, 4)))

        if not hasattr(self, "prev_touching"):
            self.prev_touching = False
        touching = (t.x != -32768)
        press = touching and not self.prev_touching
        release = (not touching) and self.prev_touching
        s = _State(touching, press, release)
        self.prev_touching = touching

        self.inputs = _Inputs(t, r, s)
        return self.inputs

    def swap(self):
        self.Display()
        self.cmd_swap()
        self.flush()
        self.cmd_dlstart()
        self.cmd_loadidentity()

    def calibrate(self):
        self.Clear()
        self.cmd_text(self.w // 2, self.h // 2, 29, 0x0600, "Tap the dot")
        self.cmd_calibrate(0)
        self.cmd_dlstart()

    def screenshot(self, dest):
        import time
        REG_SCREENSHOT_EN    = 0x302010 # Set to enable screenshot mode
        REG_SCREENSHOT_Y     = 0x302014 # Y line register
        REG_SCREENSHOT_START = 0x302018 # Screenshot start trigger
        REG_SCREENSHOT_BUSY  = 0x3020e8 # Screenshot ready flags
        REG_SCREENSHOT_READ  = 0x302174 # Set to enable readout
        RAM_SCREENSHOT       = 0x3c2000 # Screenshot readout buffer

        self.finish()

        pclk = self.rd32(REG_PCLK)
        self.wr32(REG_PCLK, 0)
        time.sleep(0.001)
        self.wr32(REG_SCREENSHOT_EN, 1)
        self.wr32(0x0030201c, 32)
        
        for ly in range(self.h):
            print(ly, "/", self.h)
            self.wr32(REG_SCREENSHOT_Y, ly)
            self.wr32(REG_SCREENSHOT_START, 1)
            time.sleep(.002)
            # while (self.raw_read(REG_SCREENSHOT_BUSY) | self.raw_read(REG_SCREENSHOT_BUSY + 4)): pass
            while self.rd(REG_SCREENSHOT_BUSY, 8) != bytes(8):
                pass
            self.wr32(REG_SCREENSHOT_READ, 1)
            bgra = self.rd(RAM_SCREENSHOT, 4 * self.w)
            rgbline = bytearray(3 * self.w)
            for i in range(self.w):
                b = bgra[4 * i + 0]
                g = bgra[4 * i + 1]
                r = bgra[4 * i + 2]
                rgbline[3 * i + 0] = r
                rgbline[3 * i + 1] = g
                rgbline[3 * i + 2] = b
            dest(rgbline)
            self.wr32(REG_SCREENSHOT_READ, 0)
        self.wr32(REG_SCREENSHOT_EN, 0)
        self.wr32(REG_PCLK, pclk)

    def screenshot_im(self):
        self.ssbytes = b""
        def appender(s):
            self.ssbytes += s
        self.screenshot(appender)
        from PIL import Image
        return Image.frombytes("RGB", (self.w, self.h), self.ssbytes)

    def load(self, f):
        while True:
            s = f.read(512)
            if not s:
                return
            self.cc(align4(s))

class MoviePlayer:
    def __init__(self, gd, f, mf_base = 0xf0000, mf_size = 0x8000):
        self.gd = gd
        self.f = f
        self.mf_base = mf_base
        self.mf_size = mf_size

        gd.cmd_mediafifo(mf_base, mf_size)
        self.wp = 0
        gd.cmd_regwrite(REG_MEDIAFIFO_WRITE, 0)

    def play(self):
        gd = self.gd
        gd.cmd_playvideo(OPT_MEDIAFIFO | OPT_FULLSCREEN | OPT_NOTEAR)
        gd.cmd_nop()
        gd.flush()
        while not gd.is_idle():
            self.service()
        gd.finish()
        
    def service(self):
        gd = self.gd

        rp = gd.rd32(REG_MEDIAFIFO_READ)
        fullness = (self.wp - rp) % self.mf_size
        SZ = 2048
        # print("rp=%x wp=%x" % (rp, self.wp))
        while fullness < (self.mf_size - SZ):
            s = self.f.read(SZ)
            if not s:
                return
            # print("Writing %x to %x" % (len(s), self.mf_base + self.wp))
            gd.wr(self.mf_base + self.wp, s)
            self.wp = (self.wp + len(s)) % self.mf_size
            gd.wr32(REG_MEDIAFIFO_WRITE, self.wp)
            fullness += len(s)
