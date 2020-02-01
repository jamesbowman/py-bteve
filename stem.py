import sys
import array
import struct

PYTHON2 = (sys.version_info < (3, 0))

B0 = b'\x00'
def align4(s):
    return s + B0 * (-len(s) & 3)

def f16(v):
    return int(round(65536 * v))

if PYTHON2:
    def packstring(s):
        return align4(s + B0)
else:
    def packstring(s):
        return align4(bytes(s, "utf-8") + B0)

def furmans(deg):
    """ Given an angle in degrees, return it in Furmans """
    return 0xffff & f16(deg / 360.0)

class EVE:

    def __init__(self, arch = '815'):
        self.buf = b''
        self.set_arch(arch)

    def set_arch(self, arch):
        assert arch in ('800', '810', '815')
        self.arch = arch
        
    def cc(self, s):
        self.buf += s
        if len(self.buf) >= 512:
            self.write(self.buf[:512])
            self.buf = self.buf[512:]

    def register(self, _):
        pass

    def flush(self):
        self.write(self.buf)
        self.buf = b''

    def c4(self, i):
        """Send a 32-bit value to the GD2."""
        self.cc(struct.pack("I", i))

    def ac(self, s):
        self.cc(align4(s))

    # The basic graphics instructions

    def AlphaFunc(self, func,ref):
        self.c4((9 << 24) | ((func & 7) << 8) | ((ref & 255)))
    def Begin(self, prim):
        self.c4((31 << 24) | ((prim & 15)))
    def BitmapHandle(self, handle):
        self.c4((5 << 24) | ((handle & 31)))
    def BitmapLayout(self, format,linestride,height):
        self.c4((7 << 24) | ((format & 31) << 19) | ((linestride & 1023) << 9) | ((height & 511)))
    def BitmapSize(self, filter,wrapx,wrapy,width,height):
        self.c4((8 << 24) | ((filter & 1) << 20) | ((wrapx & 1) << 19) | ((wrapy & 1) << 18) | ((width & 511) << 9) | ((height & 511)))
    def BitmapSource(self, addr):
        self.c4((1 << 24) | ((addr & 0xffffff)))
    def BitmapTransformA(self, a, p = 0):
        self.c4((21 << 24) | ((p & 1) << 17) | ((a & 131071)))
    def BitmapTransformB(self, b, p = 0):
        self.c4((22 << 24) | ((p & 1) << 17) | ((b & 131071)))
    def BitmapTransformC(self, c, p = 0):
        self.c4((23 << 24) | ((p & 1) << 17) | ((c & 16777215)))
    def BitmapTransformD(self, d, p = 0):
        self.c4((24 << 24) | ((p & 1) << 17) | ((d & 131071)))
    def BitmapTransformE(self, e, p = 0):
        self.c4((25 << 24) | ((p & 1) << 17) | ((e & 131071)))
    def BitmapTransformF(self, f, p = 0):
        self.c4((26 << 24) | ((p & 1) << 17) | ((f & 16777215)))
    def BlendFunc(self, src,dst):
        self.c4((11 << 24) | ((src & 7) << 3) | ((dst & 7)))
    def Call(self, dest):
        self.c4((29 << 24) | ((dest & 65535)))
    def Cell(self, cell):
        self.c4((6 << 24) | ((cell & 127)))
    def ClearColorA(self, alpha):
        self.c4((15 << 24) | ((alpha & 255)))
    def ClearColorRGB(self, red,green,blue):
        self.c4((2 << 24) | ((red & 255) << 16) | ((green & 255) << 8) | ((blue & 255)))
    def Clear(self, c = 1,s = 1,t = 1):
        self.c4((38 << 24) | ((c & 1) << 2) | ((s & 1) << 1) | ((t & 1)))
    def ClearStencil(self, s):
        self.c4((17 << 24) | ((s & 255)))
    def ClearTag(self, s):
        self.c4((18 << 24) | ((s & 255)))
    def ColorA(self, alpha):
        self.c4((16 << 24) | ((alpha & 255)))
    def ColorMask(self, r,g,b,a):
        self.c4((32 << 24) | ((r & 1) << 3) | ((g & 1) << 2) | ((b & 1) << 1) | ((a & 1)))
    def ColorRGB(self, red,green,blue):
        self.c4((4 << 24) | ((red & 255) << 16) | ((green & 255) << 8) | ((blue & 255)))
    def Display(self):
        self.c4((0 << 24))
    def End(self):
        self.c4((33 << 24))
    def Jump(self, dest):
        self.c4((30 << 24) | ((dest & 65535)))
    def LineWidth(self, width):
        self.c4((14 << 24) | ((width & 4095)))
    def Macro(self, m):
        self.c4((37 << 24) | ((m & 1)))
    def PointSize(self, size):
        self.c4((13 << 24) | ((size & 8191)))
    def RestoreContext(self):
        self.c4((35 << 24))
    def Return(self):
        self.c4((36 << 24))
    def SaveContext(self):
        self.c4((34 << 24))

    def ScissorSize(self, width,height):
        if self.arch == '800':
            self.c4((28 << 24) | ((width & 1023) << 10) | ((height & 1023)))
        else:
            self.c4((28 << 24) | ((width & 4095) << 12) | ((height & 4095)))
    def ScissorXY(self, x,y):
        if self.arch == '800':
            self.c4((27 << 24) | ((x & 511) << 9) | ((y & 511)))
        else:
            self.c4((27 << 24) | ((x & 2047) << 11) | ((y & 2047)))

    def StencilFunc(self, func,ref,mask):
        self.c4((10 << 24) | ((func & 7) << 16) | ((ref & 255) << 8) | ((mask & 255)))
    def StencilMask(self, mask):
        self.c4((19 << 24) | ((mask & 255)))
    def StencilOp(self, sfail,spass):
        self.c4((12 << 24) | ((sfail & 7) << 3) | ((spass & 7)))
    def TagMask(self, mask):
        self.c4((20 << 24) | ((mask & 1)))
    def Tag(self, s):
        self.c4((3 << 24) | ((s & 255)))
    def Vertex2f_2(self, x, y):
        x = int(2 * x)
        y = int(2 * y)
        self.c4(0x40000000 | ((x & 32767) << 15) | (y & 32767))
    def Vertex2f_4(self, x, y):
        x = int(4 * x)
        y = int(4 * y)
        self.c4(0x40000000 | ((x & 32767) << 15) | (y & 32767))
    def Vertex2f_8(self, x, y):
        x = int(8 * x)
        y = int(8 * y)
        self.c4(0x40000000 | ((x & 32767) << 15) | (y & 32767))
    def Vertex2f_16(self, x, y):
        x = int(16 * x)
        y = int(16 * y)
        self.c4(0x40000000 | ((x & 32767) << 15) | (y & 32767))

    Vertex2f = Vertex2f_16

    def Vertex2ii(self, x, y, handle = 0, cell = 0):
        self.c4((2 << 30) | ((x & 511) << 21) | ((y & 511) << 12) | ((handle & 31) << 7) | ((cell & 127)))

    # Higher-level graphics commands

    def cmd_append(self, ptr, num):
        self.cc(struct.pack("III", 0xffffff1e, ptr, num))

    def cmd_bgcolor(self, c):
        self.cc(struct.pack("II", 0xffffff09, c))

    def cmd_bitmap_transform(self, x0, y0, x1, y1, x2, y2, tx0, ty0, tx1, ty1, tx2, ty2, result):
        self.cc(struct.pack("IiiiiiiiiiiiiH", 0xffffff21, x0, y0, x1, y1, x2, y2, tx0, ty0, tx1, ty1, tx2, ty2, result))

    def cmd_button(self, x, y, w, h, font, options, s):
        self.cc(struct.pack("IhhhhhH", 0xffffff0d, x, y, w, h, font, options) + packstring(s))

    def cmd_calibrate(self, result):
        self.cc(struct.pack("II", 0xffffff15, result))

    def cmd_clock(self, x, y, r, options, h, m, s, ms):
        self.cc(struct.pack("IhhhHHHHH", 0xffffff14, x, y, r, options, h, m, s, ms))

    def cmd_coldstart(self):
        self.cc(struct.pack("I", 0xffffff32))

    def cmd_dial(self, x, y, r, options, val):
        self.cc(struct.pack("IhhhHH", 0xffffff2d, x, y, r, options, val))

    def cmd_dlstart(self):
        self.cc(struct.pack("I", 0xffffff00))

    def cmd_fgcolor(self, c):
        self.cc(struct.pack("II", 0xffffff0a, c))

    def cmd_gauge(self, x, y, r, options, major, minor, val, range):
        self.cc(struct.pack("IhhhHHHHH", 0xffffff13, x, y, r, options, major, minor, val, range))

    def cmd_getmatrix(self, a, b, c, d, e, f):
        self.cc(struct.pack("Iiiiiii", 0xffffff33, a, b, c, d, e, f))

    def cmd_getprops(self, ptr, w, h):
        self.cc(struct.pack("IIII", 0xffffff25, ptr, w, h))

    def cmd_getptr(self, result):
        self.cc(struct.pack("II", 0xffffff23, result))

    def cmd_gradcolor(self, c):
        self.cc(struct.pack("II", 0xffffff34, c))

    def cmd_gradient(self, x0, y0, rgb0, x1, y1, rgb1):
        self.cc(struct.pack("IhhIhhI", 0xffffff0b, x0, y0, rgb0, x1, y1, rgb1))

    def cmd_inflate(self, ptr):
        self.cc(struct.pack("II", 0xffffff22, ptr))

    def cmd_interrupt(self, ms):
        self.cc(struct.pack("II", 0xffffff02, ms))

    def cmd_keys(self, x, y, w, h, font, options, s):
        self.cc(struct.pack("IhhhhhH", 0xffffff0e, x, y, w, h, font, options) + packstring(s))

    def cmd_loadidentity(self):
        self.cc(struct.pack("I", 0xffffff26))

    def cmd_loadimage(self, ptr, options):
        self.cc(struct.pack("III", 0xffffff24, ptr, options))

    def cmd_logo(self):
        self.cc(struct.pack("I", 0xffffff31))

    def cmd_memcpy(self, dest, src, num):
        self.cc(struct.pack("IIII", 0xffffff1d, dest, src, num))

    def cmd_memcrc(self, ptr, num, result):
        self.cc(struct.pack("IIII", 0xffffff18, ptr, num, result))

    def cmd_memset(self, ptr, value, num):
        self.cc(struct.pack("IIII", 0xffffff1b, ptr, value, num))

    def cmd_memwrite(self, ptr, num):
        self.cc(struct.pack("III", 0xffffff1a, ptr, num))

    def cmd_regwrite(self, ptr, val):
        self.cc(struct.pack("IIII", 0xffffff1a, ptr, 4, val))

    def cmd_memzero(self, ptr, num):
        self.cc(struct.pack("III", 0xffffff1c, ptr, num))

    def cmd_number(self, x, y, font, options, n):
        self.cc(struct.pack("IhhhHi", 0xffffff2e, x, y, font, options, n))

    def cmd_progress(self, x, y, w, h, options, val, range):
        self.cc(struct.pack("IhhhhHHH", 0xffffff0f, x, y, w, h, options, val, range))

    def cmd_regread(self, ptr, result):
        self.cc(struct.pack("III", 0xffffff19, ptr, result))

    def cmd_rotate(self, a):
        self.cc(struct.pack("Ii", 0xffffff29, furmans(a)))

    def cmd_scale(self, sx, sy):
        self.cc(struct.pack("Iii", 0xffffff28, f16(sx), f16(sy)))

    def cmd_screensaver(self):
        self.cc(struct.pack("I", 0xffffff2f))

    def cmd_scrollbar(self, x, y, w, h, options, val, size, range):
        self.cc(struct.pack("IhhhhHHHH", 0xffffff11, x, y, w, h, options, val, size, range))

    def cmd_setfont(self, font, ptr):
        self.cc(struct.pack("III", 0xffffff2b, font, ptr))

    def cmd_setmatrix(self):
        self.cc(struct.pack("I", 0xffffff2a))

    def cmd_sketch(self, x, y, w, h, ptr, format):
        self.cc(struct.pack("IhhHHII", 0xffffff30, x, y, w, h, ptr, format))

    def cmd_slider(self, x, y, w, h, options, val, range):
        self.cc(struct.pack("IhhhhHHH", 0xffffff10, x, y, w, h, options, val, range))

    def cmd_snapshot(self, ptr):
        self.cc(struct.pack("II", 0xffffff1f, ptr))

    def cmd_spinner(self, x, y, style, scale):
        self.cc(struct.pack("IhhHH", 0xffffff16, x, y, style, scale))

    def cmd_stop(self):
        self.cc(struct.pack("I", 0xffffff17))

    def cmd_swap(self):
        self.cc(struct.pack("I", 0xffffff01))

    def cmd_text(self, x, y, font, options, s, *args):
        self.cc(align4(struct.pack("IhhhH", 0xffffff0c, x, y, font, options) + packstring(s)))
        return
        if PYTHON2:
            aa = array.array("I", args).tostring()
        else:
            aa = array.array("I", args).tobytes()
        self.cc(align4(struct.pack("IhhhH", 0xffffff0c, x, y, font, options) + packstring(s)) + aa)

    def cmd_toggle(self, x, y, w, font, options, state, s):
        self.cc(struct.pack("IhhhhHH", 0xffffff12, x, y, w, font, options, state) + packstring(s))

    def cmd_touch_transform(self, x0, y0, x1, y1, x2, y2, tx0, ty0, tx1, ty1, tx2, ty2, result):
        self.cc(struct.pack("IiiiiiiiiiiiiH", 0xffffff20, x0, y0, x1, y1, x2, y2, tx0, ty0, tx1, ty1, tx2, ty2, result))

    def cmd_track(self, x, y, w, h, tag):
        self.cc(struct.pack("Ihhhhhh", 0xffffff2c, x, y, w, h, tag, 0))

    def cmd_translate(self, tx, ty):
        self.cc(struct.pack("Iii", 0xffffff27, f16(tx), f16(ty)))

    # Converting versions, *f

    def cmd_translatef(self, tx, ty):
        self.cmd_translate(int(65536 * tx), int(65536 * ty))

    #
    # The new 810 opcodes
    #

    def VertexFormat(self, frac):
        self.c4((39 << 24) | (frac & 7))
        self.Vertex2f = [
            self.Vertex2f_2,
            self.Vertex2f_2,
            self.Vertex2f_4,
            self.Vertex2f_8,
            self.Vertex2f_16][frac]

    def BitmapLayoutH(self, linestride,height):
        self.c4((40 << 24) | (((linestride) & 3) << 2) | (((height) & 3)))

    def BitmapSizeH(self, width,height):
        self.c4((41 << 24) | (((width) & 3) << 2) | (((height) & 3)))

    def PaletteSource(self, addr):
        self.c4((42 << 24) | (((addr) & 4194303)))

    def VertexTranslateX(self, x):
        self.c4((43 << 24) | (((x) & 131071)))

    def VertexTranslateY(self, y):
        self.c4((44 << 24) | (((y) & 131071)))

    def Nop(self):
        self.c4((45 << 24))

    #
    # The new 810 commands
    #

    def cmd_romfont(self, dst, src):
        self.cc(struct.pack("III", 0xffffff3f, dst, src))

    def cmd_mediafifo(self, ptr, size):
        self.cc(struct.pack("III", 0xffffff39, ptr, size))

    def cmd_sync(self):
        self.cc(struct.pack("I", 0xffffff42))

    def cmd_setrotate(self, o):
        self.cc(struct.pack("II", 0xffffff36, o))

    def cmd_setbitmap(self, source, fmt, w, h):
        self.cc(struct.pack("IIHhhh", 0xffffff43, source, fmt, w, h, 0))

    def cmd_setfont2(self, font, ptr, firstchar):
        self.cc(struct.pack("IIII", 0xffffff3b, font, ptr, firstchar))

    # def cmd_snapshot2(self, 
    # def cmd_setbase(self, 
    # def cmd_playvideo(self, 
    # def cmd_setscratch(self, 
    # def cmd_videostart(self, 
    # def cmd_videoframe(self, 
    # def cmd_sync(self, 
    # def cmd_setbitmap(self, 

    def swap(self):
        self.Display()
        self.cmd_swap()
        self.flush()
        self.cmd_dlstart()
        self.cmd_loadidentity()

    # The 815 opcodes
    def BitmapExtFormat(self, fmt):
        self.c4((46 << 24) | (fmt & 65535))
    
    def BitmapSwizzle(self, r, g, b, a):
        self.c4((47 << 24) | ((r & 7) << 9) | ((g & 7) << 6) | ((b & 7) << 3) | ((a & 7)))

    # The 815 commands

    def cmd_flasherase(self):
        self.cc(struct.pack("I", 0xffffff44))

    def cmd_flashwrite(self, a, b):
        self.cc(struct.pack("III", 0xffffff45, a, len(b)) + align4(b))

    def cmd_flashupdate(self, dst, src, n):
        self.cc(struct.pack("IIII", 0xffffff47, dst, src, n))

    def cmd_flashread(self, dst, a, n):
        self.cc(struct.pack("IIII", 0xffffff46, dst, a, n))

    def cmd_flashdetach(self):
        self.cc(struct.pack("I", 0xffffff48))

    def cmd_flashattach(self):
        self.cc(struct.pack("I", 0xffffff49))

    def cmd_flashfast(self):
        self.cc(struct.pack("II", 0xffffff4a, 0xdeadbeef))

    def cmd_flashspidesel(self):
        self.cc(struct.pack("I", 0xffffff4b))

    def cmd_flashsource(self, a):
        self.cc(struct.pack("II", 0xffffff4e, a))

    def cmd_rotate_around(self, x, y, a, s = 1):
        self.cc(struct.pack("IIIII", 0xffffff51, x, y, furmans(a), int(65536 * s)))

    def cmd_inflate2(self, ptr, options):
        self.cc(struct.pack("III", 0xffffff50, ptr, options))

    def cmd_appendf(self, ptr, num):
        self.cc(struct.pack("III", 0xffffff59, ptr, num))

    def cmd_animframe(self, x, y, aoptr, frame):
        self.cc(struct.pack("IhhII", 0xffffff5a, x, y, aoptr, frame))

    def cmd_nop(self):
        self.cc(struct.pack("I", 0xffffff5b))

    # Some higher-level functions

    def calibrate(self):
        self.Clear()
        self.cmd_text(240, 135, 29, gd3.OPT_CENTER, "Tap the dot")
        self.cmd_calibrate(0)
        self.cmd_dlstart()

    def screenshot(self, dest):
        REG_SCREENSHOT_EN    = 0x302010 # Set to enable screenshot mode
        REG_SCREENSHOT_Y     = 0x302014 # Y line register
        REG_SCREENSHOT_START = 0x302018 # Screenshot start trigger
        REG_SCREENSHOT_BUSY  = 0x3020e8 # Screenshot ready flags
        REG_SCREENSHOT_READ  = 0x302174 # Set to enable readout
        RAM_SCREENSHOT       = 0x3c2000 # Screenshot readout buffer

        self.finish()
        self.unstream()

        self._wr32(REG_SCREENSHOT_EN, 1)
        self._wr32(0x0030201c, 32)
        
        self._wr32(REG_SCREENSHOT_READ, 1)

        for ly in range(self.h):
            print(ly)
            self._wr32(REG_SCREENSHOT_Y, ly)
            self._wr32(REG_SCREENSHOT_START, 1)
            time.sleep(.002)
            # while (self.raw_read(REG_SCREENSHOT_BUSY) | self.raw_read(REG_SCREENSHOT_BUSY + 4)): pass
            while self._rd(REG_SCREENSHOT_BUSY, 8) != bytes(8):
                pass
            self._wr32(REG_SCREENSHOT_READ, 1)
            bgra = self._rd(RAM_SCREENSHOT, 4 * self.w)
            (b,g,r,a) = [bgra[i::4] for i in range(4)]
            line = bytes(sum(zip(r,g,b), ()))
            dest(line)
            self._wr32(REG_SCREENSHOT_READ, 0)
        self._wr32(REG_SCREENSHOT_EN, 0)
        self.stream()

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
