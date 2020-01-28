import struct

B0 = b'\x00'
def align4(s):
    return s + B0 * (-len(s) & 3)

def f16(v):
    return int(round(65536 * v))

def packstring(s):
    return align4(bytes(s, "utf-8") + B0)

def furmans(deg):
    """ Given an angle in degrees, return it in Furmans """
    return 0xffff & f16(deg / 360.0)

class stem2(stem):

    def swap(self):
        self.Display()
        self.cmd_swap()
        self.flush()
        self.cmd_dlstart()
        self.cmd_loadidentity()

    def cmd_append(self, ptr, num):
        self.c(struct.pack("III", 0xffffff1e, ptr, num))

    def cmd_bgcolor(self, c):
        self.c(struct.pack("II", 0xffffff09, c))

    def cmd_bitmap_transform(self, x0, y0, x1, y1, x2, y2, tx0, ty0, tx1, ty1, tx2, ty2, result):
        self.c(struct.pack("IiiiiiiiiiiiiH", 0xffffff21, x0, y0, x1, y1, x2, y2, tx0, ty0, tx1, ty1, tx2, ty2, result))

    def cmd_button(self, x, y, w, h, font, options, s):
        self.c(struct.pack("IhhhhhH", 0xffffff0d, x, y, w, h, font, options) + packstring(s))

    def cmd_calibrate(self, result):
        self.c(struct.pack("II", 0xffffff15, result))

    def cmd_clock(self, x, y, r, options, h, m, s, ms):
        self.c(struct.pack("IhhhHHHHH", 0xffffff14, x, y, r, options, h, m, s, ms))

    def cmd_coldstart(self):
        self.c(struct.pack("I", 0xffffff32))

    def cmd_dial(self, x, y, r, options, val):
        self.c(struct.pack("IhhhHH", 0xffffff2d, x, y, r, options, val))

    def cmd_dlstart(self):
        self.c(struct.pack("I", 0xffffff00))

    def cmd_fgcolor(self, c):
        self.c(struct.pack("II", 0xffffff0a, c))

    def cmd_gauge(self, x, y, r, options, major, minor, val, range):
        self.c(struct.pack("IhhhHHHHH", 0xffffff13, x, y, r, options, major, minor, val, range))

    def cmd_getmatrix(self, a, b, c, d, e, f):
        self.c(struct.pack("Iiiiiii", 0xffffff33, a, b, c, d, e, f))

    def cmd_getprops(self, ptr, w, h):
        self.c(struct.pack("IIII", 0xffffff25, ptr, w, h))

    def cmd_getptr(self, result):
        self.c(struct.pack("II", 0xffffff23, result))

    def cmd_gradcolor(self, c):
        self.c(struct.pack("II", 0xffffff34, c))

    def cmd_gradient(self, x0, y0, rgb0, x1, y1, rgb1):
        self.c(struct.pack("IhhIhhI", 0xffffff0b, x0, y0, rgb0, x1, y1, rgb1))

    def cmd_inflate(self, ptr):
        self.c(struct.pack("II", 0xffffff22, ptr))

    def cmd_interrupt(self, ms):
        self.c(struct.pack("II", 0xffffff02, ms))

    def cmd_keys(self, x, y, w, h, font, options, s):
        self.c(struct.pack("IhhhhhH", 0xffffff0e, x, y, w, h, font, options) + packstring(s))

    def cmd_loadidentity(self):
        self.c(struct.pack("I", 0xffffff26))

    def cmd_loadimage(self, ptr, options):
        self.c(struct.pack("III", 0xffffff24, ptr, options))

    def cmd_logo(self):
        self.c(struct.pack("I", 0xffffff31))

    def cmd_memcpy(self, dest, src, num):
        self.c(struct.pack("IIII", 0xffffff1d, dest, src, num))

    def cmd_memcrc(self, ptr, num, result):
        self.c(struct.pack("IIII", 0xffffff18, ptr, num, result))

    def cmd_memset(self, ptr, value, num):
        self.c(struct.pack("IIII", 0xffffff1b, ptr, value, num))

    def cmd_memwrite(self, ptr, num):
        self.c(struct.pack("III", 0xffffff1a, ptr, num))

    def cmd_regwrite(self, ptr, val):
        self.c(struct.pack("IIII", 0xffffff1a, ptr, 4, val))

    def cmd_memzero(self, ptr, num):
        self.c(struct.pack("III", 0xffffff1c, ptr, num))

    def cmd_number(self, x, y, font, options, n):
        self.c(struct.pack("IhhhHi", 0xffffff2e, x, y, font, options, n))

    def cmd_progress(self, x, y, w, h, options, val, range):
        self.c(struct.pack("IhhhhHHH", 0xffffff0f, x, y, w, h, options, val, range))

    def cmd_regread(self, ptr, result):
        self.c(struct.pack("III", 0xffffff19, ptr, result))

    def cmd_rotate(self, a):
        self.c(struct.pack("Ii", 0xffffff29, furmans(a)))

    def cmd_scale(self, sx, sy):
        self.c(struct.pack("Iii", 0xffffff28, f16(sx), f16(sy)))

    def cmd_screensaver(self):
        self.c(struct.pack("I", 0xffffff2f))

    def cmd_scrollbar(self, x, y, w, h, options, val, size, range):
        self.c(struct.pack("IhhhhHHHH", 0xffffff11, x, y, w, h, options, val, size, range))

    def cmd_setfont(self, font, ptr):
        self.c(struct.pack("III", 0xffffff2b, font, ptr))

    def cmd_setmatrix(self):
        self.c(struct.pack("I", 0xffffff2a))

    def cmd_sketch(self, x, y, w, h, ptr, format):
        self.c(struct.pack("IhhHHII", 0xffffff30, x, y, w, h, ptr, format))

    def cmd_slider(self, x, y, w, h, options, val, range):
        self.c(struct.pack("IhhhhHHH", 0xffffff10, x, y, w, h, options, val, range))

    def cmd_snapshot(self, ptr):
        self.c(struct.pack("II", 0xffffff1f, ptr))

    def cmd_spinner(self, x, y, style, scale):
        self.c(struct.pack("IhhHH", 0xffffff16, x, y, style, scale))

    def cmd_stop(self):
        self.c(struct.pack("I", 0xffffff17))

    def cmd_swap(self):
        self.c(struct.pack("I", 0xffffff01))

    def cmd_text(self, x, y, font, options, s, *args):
        self.c(align4(struct.pack("IhhhH", 0xffffff0c, x, y, font, options) + packstring(s)))
        return
        if PYTHON2:
            aa = array.array("I", args).tostring()
        else:
            aa = array.array("I", args).tobytes()
        self.c(align4(struct.pack("IhhhH", 0xffffff0c, x, y, font, options) + packstring(s)) + aa)

    def cmd_toggle(self, x, y, w, font, options, state, s):
        self.c(struct.pack("IhhhhHH", 0xffffff12, x, y, w, font, options, state) + packstring(s))

    def cmd_touch_transform(self, x0, y0, x1, y1, x2, y2, tx0, ty0, tx1, ty1, tx2, ty2, result):
        self.c(struct.pack("IiiiiiiiiiiiiH", 0xffffff20, x0, y0, x1, y1, x2, y2, tx0, ty0, tx1, ty1, tx2, ty2, result))

    def cmd_track(self, x, y, w, h, tag):
        self.c(struct.pack("Ihhhhhh", 0xffffff2c, x, y, w, h, tag, 0))

    def cmd_translate(self, tx, ty):
        self.c(struct.pack("Iii", 0xffffff27, f16(tx), f16(ty)))

    def cmd_translatef(self, tx, ty):
        self.cmd_translate(int(65536 * tx), int(65536 * ty))

    #
    # 810 commands
    #

    """
    def VertexFormat(self, frac):
        self.c4((39 << 24) | (frac & 7))
        self.Vertex2f = [
            self.Vertex2f_2,
            self.Vertex2f_2,
            self.Vertex2f_4,
            self.Vertex2f_8,
            self.Vertex2f_16][frac]

    """
    def Vertex2f(self, x, y):
        x = int(16 * x)
        y = int(16 * y)
        self.c(struct.pack("I", 0x40000000 | ((x & 32767) << 15) | (y & 32767)))

    #
    # The new 810 commands
    #

    def cmd_romfont(self, dst, src):
        self.c(struct.pack("III", 0xffffff3f, dst, src))

    def cmd_mediafifo(self, ptr, size):
        self.c(struct.pack("III", 0xffffff39, ptr, size))

    def cmd_sync(self):
        self.c(struct.pack("I", 0xffffff42))

    def cmd_setrotate(self, o):
        self.c(struct.pack("II", 0xffffff36, o))

    def cmd_setbitmap(self, source, fmt, w, h):
        self.c(struct.pack("IIHhhh", 0xffffff43, source, fmt, w, h, 0))

    def cmd_setfont2(self, font, ptr, firstchar):
        self.c(struct.pack("IIII", 0xffffff3b, font, ptr, firstchar))

    # def cmd_snapshot2(self, 
    # def cmd_setbase(self, 
    # def cmd_playvideo(self, 
    # def cmd_setscratch(self, 
    # def cmd_videostart(self, 
    # def cmd_videoframe(self, 
    # def cmd_sync(self, 
    # def cmd_setbitmap(self, 

    #
    # 815 commands
    #

    def cmd_flasherase(self):
        self.c(struct.pack("I", 0xffffff44))

    def cmd_flashwrite(self, a, b):
        self.c(struct.pack("III", 0xffffff45, a, len(b)) + align4(b))

    def cmd_flashupdate(self, dst, src, n):
        self.c(struct.pack("IIII", 0xffffff47, dst, src, n))

    def cmd_flashread(self, dst, a, n):
        self.c(struct.pack("IIII", 0xffffff46, dst, a, n))

    def cmd_flashdetach(self):
        self.c(struct.pack("I", 0xffffff48))

    def cmd_flashattach(self):
        self.c(struct.pack("I", 0xffffff49))

    def cmd_flashfast(self):
        self.c(struct.pack("II", 0xffffff4a, 0xdeadbeef))

    def cmd_flashspidesel(self):
        self.c(struct.pack("I", 0xffffff4b))

    def cmd_flashsource(self, a):
        self.c(struct.pack("II", 0xffffff4e, a))

    def cmd_rotate_around(self, x, y, a, s = 1):
        self.c(struct.pack("IIIII", 0xffffff51, x, y, furmans(a), int(65536 * s)))

    def cmd_inflate2(self, ptr, options):
        self.c(struct.pack("III", 0xffffff50, ptr, options))

    def cmd_appendf(self, ptr, num):
        self.c(struct.pack("III", 0xffffff59, ptr, num))

    def cmd_animframe(self, x, y, aoptr, frame):
        self.c(struct.pack("IhhII", 0xffffff5a, x, y, aoptr, frame))

    def cmd_nop(self):
        self.c(struct.pack("I", 0xffffff5b))

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

        self.wr32(REG_SCREENSHOT_EN, 1)
        self.wr32(0x0030201c, 32)
        
        self.wr32(REG_SCREENSHOT_READ, 1)

        for ly in range(self.h):
            print(ly)
            self.wr32(REG_SCREENSHOT_Y, ly)
            self.wr32(REG_SCREENSHOT_START, 1)
            time.sleep(.002)
            # while (self.raw_read(REG_SCREENSHOT_BUSY) | self.raw_read(REG_SCREENSHOT_BUSY + 4)): pass
            while self.rd(REG_SCREENSHOT_BUSY, 8) != bytes(8):
                pass
            self.wr32(REG_SCREENSHOT_READ, 1)
            bgra = self.rd(RAM_SCREENSHOT, 4 * self.w)
            (b,g,r,a) = [bgra[i::4] for i in range(4)]
            line = bytes(sum(zip(r,g,b), ()))
            dest(line)
            self.wr32(REG_SCREENSHOT_READ, 0)
        self.wr32(REG_SCREENSHOT_EN, 0)
