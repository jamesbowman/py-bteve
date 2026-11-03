import random
import bteve as eve
import apprunner

rr = random.randrange


def fizz(gd):
    while True:
        gd.Clear()
        gd.Begin(eve.POINTS)
        for i in range(100):
            gd.ColorRGB(rr(256), rr(256), rr(256))
            gd.PointSize(rr(100))
            gd.Vertex2f(rr(gd.w), rr(gd.h))
        gd.swap()


if __name__ == "__main__":
    apprunner.run(fizz)
