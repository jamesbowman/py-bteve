"""Animated line trails, scaled to the connected display."""

import math
import random
import time

import apprunner
import bteve as eve


def tri(t):
    return 2 * abs(math.fmod(t, 1.0) - 0.5)


def qix(gd, frames=None):
    frequencies = [random.random() for _ in range(9)]

    def at(t, ff):
        gd.Vertex2f(gd.w * tri(ff[0] * t), gd.h * tri(ff[1] * t))

    frame = 0
    while frames is None or frame < frames:
        t = time.monotonic() / 0.018
        gd.Clear()
        gd.VertexFormat(3)
        gd.LineWidth(3)
        for dt in range(0, 30, 3):
            gd.Begin(eve.LINE_STRIP)
            tn = (t - dt) / 150
            gd.ColorRGB(*(int(255 * tri(f * tn)) for f in frequencies[6:9]))
            for pair in (frequencies[0:2], frequencies[2:4],
                         frequencies[4:6], frequencies[0:2]):
                at(tn, pair)
        gd.swap()
        frame += 1


if __name__ == "__main__":
    apprunner.run(qix)
