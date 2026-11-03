from pathlib import Path
import apprunner
import math
import bteve as eve

def norm(L):
    m = max(L)
    return [e / m for e in L]

# Draw a full-screen circular gradient in the current color
# Uses a product-of-gaussians, see
#   https://excamera.com/sphinx/article-circular.html
# for the math.

def setup_circular(gd):
    # Write a 1-D gaussian bitmap to address 0
    w = max(gd.w, gd.h)
    xx = [-1 + 2 * x / w for x in range(w)]
    c = math.sqrt(.45)
    gauss = norm([math.exp(-(x*x) / (2 * c ** 2)) for x in xx])
    gd.cmd_memwrite(0, len(gauss))
    gd.cc(eve.align4(bytes([int(255 * e) for e in gauss])))

def draw_circular(gd):
    # Draw gaussian in X and Y multiplied to create a circular gradient

    w = max(gd.w, gd.h)
    gd.SaveContext()
    gd.BitmapHandle(15)
    gd.Begin(eve.BITMAPS)

    # Draw in X, in replace mode. Only care about the Alpha channel
    gd.BlendFunc(1, 0)
    gd.cmd_setbitmap(0, eve.L8, w, 1)
    gd.BitmapSize(eve.NEAREST, eve.BORDER, eve.REPEAT, w, w)
    gd.BitmapSizeH(w >> 9, w >> 9)
    gd.Vertex2f(0, (gd.h - w) / 2)

    # Multiply by gaussian in Y, again only care about the alpha channel
    gd.BlendFunc(eve.DST_ALPHA, 0)
    gd.cmd_setbitmap(0, eve.L8, 1, w)
    gd.BitmapSize(eve.NEAREST, eve.REPEAT, eve.BORDER, w, w)
    gd.BitmapSizeH(w >> 9, w >> 9)
    gd.Vertex2f(0, (gd.h - w) / 2)

    # Now paint the whole screen, scaled by the alpha channel value
    gd.Begin(eve.RECTS)
    gd.Vertex2f(0, 0)
    gd.Vertex2f(gd.w, gd.h)
    gd.RestoreContext()

def rotoblinka(gd, frames=None):
    assetdir = Path(__file__).resolve().parents[1] / "assets"
    setup_circular(gd)

    gd.BitmapHandle(0)
    gd.cmd_loadimage(2048, 0)
    with (assetdir / "blinka540.png").open("rb") as source:
        gd.load(source)
    gd.BitmapHandle(1)
    gd.cmd_loadimage(-1, 0)  # Let EVE append after the previous decoded image.
    with (assetdir / "circuitpython.png").open("rb") as source:
        gd.load(source)
    panel_scale = min(gd.w, gd.h) / 720

    def ring(scale, t):
        # Draw a ring of 10 blinkas, 36 degrees apart
        r = min(gd.w, gd.h) * 0.34
        for i in range(10):
            angle = 360 * i / 10 + t
            gd.cmd_loadidentity()
            gd.cmd_rotatearound(540 // 2, 540 // 2, angle, scale * panel_scale * 0.30)
            gd.cmd_setmatrix()
            th = math.radians(-angle)
            x = scale * r * math.sin(th)
            y = scale * r * math.cos(th)
            gd.Vertex2f(x, y)

    t = 7
    frame = 0
    while frames is None or frame < frames:
        gd.VertexFormat(2)
        gd.Clear()

        # Bluish background glow
        gd.ColorRGB(0x40, 0x50, 0x70)
        draw_circular(gd)

        gd.Begin(eve.BITMAPS)

        gd.SaveContext()        # {
        gd.BitmapHandle(0)      # blinka540.png

        # Translate so (0, 0) draws a Blinka at screen center
        gd.VertexTranslateX((gd.w - 540) / 2)
        gd.VertexTranslateY((gd.h - 540) / 2)

        # Inner ring, slightly darker
        gd.ColorRGB(0xb0, 0xb0, 0xc0)
        ring(0.70, -2 * t)

        # Outer ring, full brightness
        gd.ColorRGB(0xff, 0xff, 0xff)
        ring(1.00, t)
        gd.RestoreContext()     # }


        # Central logo
        gd.BitmapHandle(1)      # circuitpython.png
        gd.ColorRGB(0xff, 0xff, 0xff)
        gd.cmd_loadidentity()
        gd.cmd_rotatearound(364 // 2, 395 // 2, 0, panel_scale * 0.70)
        gd.cmd_setmatrix()
        gd.Vertex2f((gd.w - 364) / 2, (gd.h - 395) / 2)

        gd.swap()
        t += 0.5
        frame += 1


if __name__ == "__main__":
    apprunner.run(rotoblinka)
