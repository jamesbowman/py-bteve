import os
import unittest
from binascii import crc32

import bteve as eve

class MockSPIDriver:
    def unsel(self):
        assert 0
        pass
    def sel(self):
        pass
    def write(self):
        pass
    def seta(self, x):
        pass
    def setb(self, x):
        pass

class Dumper(eve.Gameduino):
    def __init__(self):
        self.d = []
    def cc(self, bb):
        self.d.append(bb)

def cov0(gd):
    perms = [
        (0,0,0,0,0),
        (1,1,1,1,1),
        (-1,-1,-1,-1,-1),
        (0,1,0,1,0),
        (1,2,3,4,5),
        (0, 0, 0, 0, -1),
        (0, 0, 0, -1, 0),
        (0, 0, -1, 0, 0),
        (0, -1, 0, 0, 0),
        (-1, 0, 0, 0, 0),
        (0x55555, 0x55555, 0x55555, 0x55555, 0x55555),
        (0xaaaaa, 0xaaaaa, 0xaaaaa, 0xaaaaa, 0xaaaaa),
    ]
    for (a,b,c,d,e) in perms:
        gd.AlphaFunc(a,b)
        gd.Begin(a)
        gd.BitmapExtFormat(a)
        gd.BitmapHandle(a)
        gd.BitmapLayoutH(a,b)
        gd.BitmapLayout(a,b,c)
        gd.BitmapSizeH(a,b)
        gd.BitmapSize(a,b,c,d,e)
        gd.BitmapSource(a)
        gd.BitmapSwizzle(a,b,c,d)
        gd.BitmapTransformA(a,b)
        gd.BitmapTransformB(a,b)
        gd.BitmapTransformC(a,b)
        gd.BitmapTransformD(a,b)
        gd.BitmapTransformE(a,b)
        gd.BitmapTransformF(a,b)
        gd.BlendFunc(a,b)
        gd.Call(a)
        gd.Cell(a)
        gd.ClearColorA(a)
        gd.ClearColorRGB(a,b,c)
        gd.Clear(a,b,c)
        gd.ClearStencil(a)
        gd.ClearTag(a)
        gd.ColorA(a)
        gd.ColorMask(a,b,c,d)
        gd.ColorRGB(a,b,c)
        gd.Display()
        gd.End()
        gd.Jump(a)
        gd.LineWidth(a)
        gd.Macro(a)
        gd.Nop()
        gd.PaletteSource(a)
        gd.PointSize(a)
        gd.RestoreContext()
        gd.Return()
        gd.SaveContext()
        gd.ScissorSize(a,b)
        gd.ScissorXY(a,b)
        gd.StencilFunc(a,b,c)
        gd.StencilMask(a)
        gd.StencilOp(a,b)
        gd.TagMask(a)
        gd.Tag(a)
        gd.VertexTranslateX(a)
        gd.VertexTranslateY(a)

    perms13 = [
        (0,) * 13,
        (1,2,3,4,5,6,7,8,9,10,11,12,13)
    ]

    for (a,b,c,d,e,f,g,h,i,j,k,l,m) in perms13:
        gd.cmd_animframe(a,b,c,d)
        gd.cmd_append(a,b)
        gd.cmd_appendf(a,b)
        gd.cmd_bgcolor(a)
        gd.cmd_bitmap_transform(a,b,c,d,e,f,g,h,i,j,k,l,m)
        gd.cmd_calibrate(a)
        gd.cmd_clock(a,b,c,d,e,f,g,h)
        gd.cmd_coldstart()
        gd.cmd_dial(a,b,c,d,e)
        gd.cmd_dlstart()
        gd.cmd_fgcolor(a)
        gd.cmd_flashattach()
        gd.cmd_flashdetach()
        gd.cmd_flasherase()
        gd.cmd_flashfast()
        gd.cmd_flashread(a,b,c)
        gd.cmd_flashsource(a)
        gd.cmd_flashspidesel()
        gd.cmd_flashupdate(a,b,c)
        gd.cmd_gauge(a,b,c,d,e,f,g,h)
        gd.cmd_getmatrix(a,b,c,d,e,f)
        gd.cmd_getprops(a,b,c)
        gd.cmd_getptr(a)
        gd.cmd_gradcolor(a)
        gd.cmd_gradient(a,b,c,d,e,f)
        gd.cmd_inflate2(a,b)
        gd.cmd_inflate(a)
        gd.cmd_interrupt(a)
        gd.cmd_loadidentity()
        gd.cmd_loadimage(a,b)
        gd.cmd_logo()
        gd.cmd_mediafifo(a,b)
        gd.cmd_memcpy(a,b,c)
        gd.cmd_memcrc(a,b,c)
        gd.cmd_memset(a,b,c)
        gd.cmd_memwrite(a,b)
        gd.cmd_memzero(a,b)
        gd.cmd_nop()
        gd.cmd_number(a,b,c,d,e)
        gd.cmd_progress(a,b,c,d,e,f,g)
        gd.cmd_regread(a,b)
        gd.cmd_romfont(a,b)
        gd.cmd_rotate(a)
        gd.cmd_rotatearound(a,b,c,d)
        gd.cmd_scale(a,b)
        gd.cmd_screensaver()
        gd.cmd_scrollbar(a,b,c,d,e,f,g,h)
        gd.cmd_setbase(a)
        gd.cmd_setbitmap(a,b,c,d)
        gd.cmd_setfont2(a,b,c)
        gd.cmd_setfont(a,b)
        gd.cmd_setmatrix()
        gd.cmd_setrotate(a)
        gd.cmd_setscratch(a)
        gd.cmd_sketch(a,b,c,d,e,f)
        gd.cmd_slider(a,b,c,d,e,f,g)
        gd.cmd_snapshot2(a,b,c,d,e,f)
        gd.cmd_snapshot(a)
        gd.cmd_spinner(a,b,c,d)
        gd.cmd_stop()
        gd.cmd_swap()
        gd.cmd_sync()
        gd.cmd_touch_transform(a,b,c,d,e,f,g,h,i,j,k,l,m)
        gd.cmd_track(a,b,c,d,e)
        gd.cmd_translate(a,b)
        gd.cmd_videoframe(a,b)
        gd.cmd_videostart()
        gd.cmd_videostartf()

    gd.cmd_flashwrite(0x55, b"1234")
    gd.cmd_flashwrite(0x55, b"12345678")

    for (a,b,c,d,e,f,g,h,i,j,k,l,m) in perms13:
        for s in ("", "1", "12", "123", "1234", "something"):
            gd.cmd_keys(a,b,c,d,e,f,s)
            gd.cmd_toggle(a,b,c,d,e,f,s,s)
            gd.cmd_button(a,b,c,d,e,f,s)
            gd.cmd_text(a,b,c,d,s)

            gd.cmd_text(a,b,c,d,s, g)
            gd.cmd_text(a,b,c,d,s, g,h)
            gd.cmd_text(a,b,c,d,s, g,h,i)

    with open("assets/blinka100.png", "rb") as f:
        gd.load(f)

class TestPure(unittest.TestCase):

    def test_wii_classic_pro(self):
        gd = Dumper()
        inert = bytes([160, 32, 16, 0, 255, 255])
        g = gd.wii_classic_pro(inert)
        self.assertEqual(tuple(g.joysticks), (16, 16, 32, 32))
        self.assertEqual(g.joysticks.rx     , 16)
        self.assertEqual(g.joysticks.ry     , 16)
        self.assertEqual(g.joysticks.lx     , 32)
        self.assertEqual(g.joysticks.ly     , 32)
        self.assertEqual(g.buttons.A        , 0)
        self.assertEqual(g.buttons.B        , 0)
        self.assertEqual(g.buttons.X        , 0)
        self.assertEqual(g.buttons.Y        , 0)
        self.assertEqual(g.buttons.R        , 0)
        self.assertEqual(g.buttons.L        , 0)
        self.assertEqual(g.buttons.ZR       , 0)
        self.assertEqual(g.buttons.ZL       , 0)
        self.assertEqual(g.buttons.start    , 0)
        self.assertEqual(g.buttons.select   , 0)
        self.assertEqual(g.buttons.home     , 0)
        self.assertEqual(g.buttons.plus     , 0)
        self.assertEqual(g.buttons.minus    , 0)
        self.assertEqual(g.dpad.up          , 0)
        self.assertEqual(g.dpad.down        , 0)
        self.assertEqual(g.dpad.right       , 0)
        self.assertEqual(g.dpad.left        , 0)
        self.assertEqual(g.triggers.right   , 0)
        self.assertEqual(g.triggers.left    , 0)

        all_buttons = bytes([160, 32, 16, 0, 0, 0])
        g = gd.wii_classic_pro(all_buttons)
        self.assertTrue(all(g.buttons))

    def test_coverage(self):
        gd = Dumper()
        cov0(gd)
        actual = crc32(b"".join(gd.d))
        self.assertEqual(actual, 0x3adadb18, hex(actual))

if __name__ == '__main__':
    unittest.main()

