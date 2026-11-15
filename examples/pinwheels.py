import math
import bteve as eve
import apprunner

def pinwheels(gd):
    def wheel(i, r, npoints):
        r = r * gd.h / 480
        step = 2 * math.pi * 17 / npoints
        theta = i / r
        gd.Begin(eve.LINE_STRIP)
        for i in range(npoints + 1):
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            gd.Vertex2f(x, y)
            theta += step

    for i in range(9999999):
        gd.Clear()
        # gd.cmd_cgradient( eve.CORNER_ZERO, 0, (gd.h - gd.w) // 2, gd.w, gd.w, 0x000000, 0x402020)
        gd.VertexTranslateX(gd.w // 2)
        gd.VertexTranslateY(gd.h // 2)

        gd.ColorRGB(0xc0, 0xff, 0xc0)
        wheel(i, 30, 30)
        gd.ColorRGB(0xff, 0xff, 0xc0)
        wheel(i, 48, 20)
        gd.ColorRGB(0xff, 0xc0, 0xc0)
        wheel(i, 110, 13)
        gd.ColorRGB(0xc0, 0xc0, 0xff)
        wheel(i, 230, 52)
        gd.swap()

apprunner.run(pinwheels)
