"""Draw on the touchscreen. The sketch engine keeps running after Python exits."""

import apprunner
import bteve as eve


def sketch(gd):
    # L1 rows occupy whole bytes, including on panels whose width is not / 8.
    size = ((gd.w + 7) // 8) * gd.h
    gd.cmd_memzero(0, size)
    gd.cmd_sketch(0, 0, gd.w, gd.h, 0, eve.L1)
    gd.ClearColorRGB(0x18, 0x20, 0x30)
    gd.Clear()
    gd.ColorRGB(255, 255, 255)
    gd.cmd_setbitmap(0, eve.L1, gd.w, gd.h)
    gd.Begin(eve.BITMAPS)
    gd.Vertex2f(0, 0)
    gd.cmd_text(gd.w // 2, 24, 27, eve.OPT_CENTER, "Draw on the screen")
    gd.swap()


if __name__ == "__main__":
    apprunner.run(sketch)
