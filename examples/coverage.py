class MockFile:
    def __init__(self, len):
        self.rem = len
    def read(self, sz):
        n = min(sz, self.rem)
        self.rem -= n
        return b"U" * n

def cov0(eve):
    perms = [
        (0,0,0,0,0),
        (1,1,1,1,1),
        (-1,-1,-1,-1,-1),
        (0,1,0,1,0),
        (1,2,3,4,5),
        (0x55555, 0x55555, 0x55555, 0x55555, 0x55555),
    ]
    for (a,b,c,d,e) in perms:
        eve.AlphaFunc(a,b)
        eve.Begin(a)
        eve.BitmapExtFormat(a)
        eve.BitmapHandle(a)
        eve.BitmapLayoutH(a,b)
        eve.BitmapLayout(a,b,c)
        eve.BitmapSizeH(a,b)
        eve.BitmapSize(a,b,c,d,e)
        eve.BitmapSource(a)
        eve.BitmapSwizzle(a,b,c,d)
        eve.BitmapTransformA(a,b)
        eve.BitmapTransformB(a,b)
        eve.BitmapTransformC(a,b)
        eve.BitmapTransformD(a,b)
        eve.BitmapTransformE(a,b)
        eve.BitmapTransformF(a,b)
        eve.BlendFunc(a,b)
        eve.Call(a)
        eve.Cell(a)
        eve.ClearColorA(a)
        eve.ClearColorRGB(a,b,c)
        eve.Clear(a,b,c)
        eve.ClearStencil(a)
        eve.ClearTag(a)
        eve.ColorA(a)
        eve.ColorMask(a,b,c,d)
        eve.ColorRGB(a,b,c)
        eve.Display()
        eve.End()
        eve.Jump(a)
        eve.LineWidth(a)
        eve.Macro(a)
        eve.Nop()
        eve.PaletteSource(a)
        eve.PointSize(a)
        eve.RestoreContext()
        eve.Return()
        eve.SaveContext()
        eve.ScissorSize(a,b)
        eve.ScissorXY(a,b)
        eve.StencilFunc(a,b,c)
        eve.StencilMask(a)
        eve.StencilOp(a,b)
        eve.TagMask(a)
        eve.Tag(a)
        eve.VertexTranslateX(a)
        eve.VertexTranslateY(a)

    perms13 = [
        (0,) * 13,
        (1,2,3,4,5,6,7,8,9,10,11,12,13)
    ]

    for (a,b,c,d,e,f,g,h,i,j,k,l,m) in perms13:
        eve.cmd_animframe(a,b,c,d)
        eve.cmd_append(a,b)
        eve.cmd_appendf(a,b)
        eve.cmd_bgcolor(a)
        eve.cmd_bitmap_transform(a,b,c,d,e,f,g,h,i,j,k,l,m)
        eve.cmd_calibrate(a)
        eve.cmd_clock(a,b,c,d,e,f,g,h)
        eve.cmd_coldstart()
        eve.cmd_dial(a,b,c,d,e)
        eve.cmd_dlstart()
        eve.cmd_fgcolor(a)
        eve.cmd_flashattach()
        eve.cmd_flashdetach()
        eve.cmd_flasherase()
        eve.cmd_flashfast()
        eve.cmd_flashread(a,b,c)
        eve.cmd_flashsource(a)
        eve.cmd_flashspidesel()
        eve.cmd_flashupdate(a,b,c)
        eve.cmd_gauge(a,b,c,d,e,f,g,h)
        eve.cmd_getmatrix(a,b,c,d,e,f)
        eve.cmd_getprops(a,b,c)
        eve.cmd_getptr(a)
        eve.cmd_gradcolor(a)
        eve.cmd_gradient(a,b,c,d,e,f)
        eve.cmd_inflate2(a,b)
        eve.cmd_inflate(a)
        eve.cmd_interrupt(a)
        eve.cmd_loadidentity()
        eve.cmd_loadimage(a,b)
        eve.cmd_logo()
        eve.cmd_mediafifo(a,b)
        eve.cmd_memcpy(a,b,c)
        eve.cmd_memcrc(a,b,c)
        eve.cmd_memset(a,b,c)
        eve.cmd_memwrite(a,b)
        eve.cmd_memzero(a,b)
        eve.cmd_nop()
        eve.cmd_number(a,b,c,d,e)
        eve.cmd_progress(a,b,c,d,e,f,g)
        eve.cmd_regread(a,b)
        eve.cmd_romfont(a,b)
        eve.cmd_rotate(a)
        eve.cmd_rotatearound(a,b,c,d)
        eve.cmd_scale(a,b)
        eve.cmd_screensaver()
        eve.cmd_scrollbar(a,b,c,d,e,f,g,h)
        eve.cmd_setbase(a)
        eve.cmd_setbitmap(a,b,c,d)
        eve.cmd_setfont2(a,b,c)
        eve.cmd_setfont(a,b)
        eve.cmd_setmatrix()
        eve.cmd_setrotate(a)
        eve.cmd_setscratch(a)
        eve.cmd_sketch(a,b,c,d,e,f)
        eve.cmd_slider(a,b,c,d,e,f,g)
        eve.cmd_snapshot2(a,b,c,d,e,f)
        eve.cmd_snapshot(a)
        eve.cmd_spinner(a,b,c,d)
        eve.cmd_stop()
        eve.cmd_swap()
        eve.cmd_sync()
        eve.cmd_touch_transform(a,b,c,d,e,f,g,h,i,j,k,l,m)
        eve.cmd_track(a,b,c,d,e)
        eve.cmd_translate(a,b)
        eve.cmd_videoframe(a,b)
        eve.cmd_videostart()
        eve.cmd_videostartf()

    eve.cmd_flashwrite(0x55, b"1234")
    eve.cmd_flashwrite(0x55, b"12345678")

    for (a,b,c,d,e,f,g,h,i,j,k,l,m) in perms13:
        for s in ("", "1", "12", "123", "1234", "something"):
            eve.cmd_keys(a,b,c,d,e,f,s)
            eve.cmd_toggle(a,b,c,d,e,f,s)
            eve.cmd_button(a,b,c,d,e,f,s)
            eve.cmd_text(a,b,c,d,s)

            # XXX MicroPython is currently lacking array.array.tobytes()
            # eve.cmd_text(a,b,c,d,s, g)
            # eve.cmd_text(a,b,c,d,s, g,h)
            # eve.cmd_text(a,b,c,d,s, g,h,i)

    for l in (0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 785):
        rd = MockFile(l)
        eve.load(rd)
    """
    f.load(open("circuitpython.png", "rb"))
    """
