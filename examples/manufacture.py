import sys
import time
import struct
import bteve as eve
from spidriver import SPIDriver

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

dev = "43"

if dev == "43":
    settings = {
     eve.REG_CSPREAD: 1,
     eve.REG_DITHER: 1,
     eve.REG_PCLK_POL: 1,

     eve.REG_ROTATE: 1,
     eve.REG_OUTBITS: (64 + 8 + 1) * 6,
     eve.REG_SWIZZLE: 3,
     0x003020e4: 4,     # select PWM

     eve.REG_PCLK: 6,
    }
else:
    settings = {
     eve.REG_HCYCLE: 969,   # was 928
     eve.REG_HOFFSET: 88,
     eve.REG_HSIZE: 800,
     eve.REG_HSYNC0: 0,
     eve.REG_HSYNC1: 48,

     eve.REG_VCYCLE: 516,
     eve.REG_VOFFSET: 32,
     eve.REG_VSIZE: 480,
     eve.REG_VSYNC0: 0,
     eve.REG_VSYNC1: 3,

     eve.REG_CSPREAD: 0,
     eve.REG_DITHER: 1,
     eve.REG_PCLK_POL: 1,
     eve.REG_PCLK: 2,

     eve.REG_ROTATE: 1,
     eve.REG_OUTBITS: (64 + 8 + 1) * 6,
     eve.REG_SWIZZLE: 3,
     0x003020e4: 4,     # select PWM
    }

def bars(gd, msg = None):
    x0 = int(.2 * gd.w)
    x1 = int(.8 * gd.w)
    H = 20
    Y = 30
    y = 60
    for i,(cname, rgb) in enumerate([("red", 0xff0000), ("green", 0xff00), ("blue", 0xff), ("white", 0xffffff)]):
        gd.SaveContext()
        gd.ScissorSize(x1 - x0, H)
        gd.ScissorXY(x0, y)
        gd.cmd_gradient(x0, 0, 0x000000, x1, 0, rgb)
        gd.RestoreContext()
        y += Y
    if msg is not None:
        gd.cmd_text(gd.w // 2, int(.85 * gd.h), 30, eve.OPT_CENTER, msg)

def fail(s):
    print()
    print('>>>>>>> ' + s)
    print()
    sys.exit(1)

def calibrate(gd):
    s_sketch = gd.w * gd.h // 8

    if gd.rd32(eve.REG_FLASH_STATUS) != 2:
        fail("Bad flash")

    if 1:
        gd.cmd_dlstart()
        gd.Clear()
        bars(gd, 'CALIBRATE')
        gd.cmd_calibrate(0)
        gd.cmd_dlstart()
        print('waiting for calibration')
        gd.finish()

    tsc = gd.rd(eve.REG_TOUCH_TRANSFORM_A, 24)

    if 1:
        cap = Gameduino()

        cap.cmd_regwrite(eve.REG_FREQUENCY, 60000000)
        cap.cmd_memwrite(eve.REG_TOUCH_TRANSFORM_A, 24)
        print(list(tsc))
        cap.cc(tsc)
        for (r, v) in settings.items():
            cap.cmd_regwrite(r, v)
        cap.pack()
    
    f8k = open("unified.blob", "rb").read() + cap.buf
    assert len(f8k) == 8192
    gd.cmd_memwrite(0, len(f8k))
    gd.cc(f8k)
    gd.cmd_flashupdate(0, 0, len(f8k))

    gd.cmd_flashfast()
    if gd.result() != 0 or gd.rd32(eve.REG_FLASH_STATUS) != 3:
        fail("Flash did not enter fast mode")

    gd.cmd_memzero(0, s_sketch)
    gd.cmd_sketch(0, 0, gd.w, gd.h, 0, eve.L1)

    gd.Clear()
    bars(gd)
    gd.cmd_setbitmap(0, eve.L1, gd.w, gd.h)
    gd.Begin(eve.BITMAPS)
    gd.Vertex2f(0, 0)
    gd.Tag(97)
    gd.cmd_button(
        int(.40 * gd.w), 0,
        int(.2 * gd.w), int(.2 * gd.h),
        28, eve.OPT_FLAT, "DONE")
    gd.swap()

    gd.finish()
    while gd.rd32(eve.REG_TOUCH_TAG) != 97:
        pass
    return

    gd.bars("Please initial then tap DONE")

    gd.cmd_setbitmap(0, eve.L1, eve.w, eve.h)
    gd.Begin(eve.BITMAPS)

    if gd.dc:
        gd.Vertex2ii(0, 0, 1, 0)
    gd.Vertex2f(0, 0)
    gd.cmd_memwrite(eve.REG_MACRO_0, 4)
    gd.ColorRGB(0, 0, 0)
    gd.Macro(0)
    gd.Tag(97)
    gd.cmd_button(
        int(.40 * gd.w), 0,
        int(.2 * gd.w), int(.2 * gd.h),
        28, eve.OPT_FLAT, "DONE")
    gd.swap()

    if gd.dc:
        eve.wr(gd.co, gd.dc)

    gd.cmd_memwrite(eve.REG_MACRO_0, 4)
    gd.ColorRGB(255, 255, 255)
    gd.flush()

    while gd.rd32(eve.REG_TOUCH_TAG) != 97:
        pass

    gd.cmd_stop()
    gd.write_lower(s_sketch)
    if 0:
        gd.Clear(1,1,1)
        gd.bars("readback")
        gd.swap()

        t0 = time.time()
        Image.frombytes("1", (gd.w, gd.h), gd.rd(0, s_sketch)).save("out.png")
        t1 = time.time()
        print('readback', t1 - t0)

if __name__ == "__main__":
    gd = eve.GameduinoSPIDriver(SPIDriver(sys.argv[1]))
    gd.register(gd)
    gd.coldstart()

    t0 = time.time()
    while gd.rd32(eve.REG_ID) != 0x7c:
        assert (time.time() - t0) < 1.0, "No response - is device attached?"
    print('have ID')
    gd.getspace()

    gd.Clear()
    gd.swap()
    for (r, v) in settings.items():
        gd.cmd_regwrite(r, v)
    gd.cmd_regwrite(eve.REG_GPIO, 0x83)
    gd.ClearColorRGB(0x20, 0x40, 0x20)
    gd.Clear()
    (gd.w, gd.h) = (480, 272)
    gd.cmd_text(gd.w // 2, gd.h // 2, 31, eve.OPT_CENTER, "Hello world")
    gd.swap()
    gd.finish()

    calibrate(gd)
    sys.exit(0)
