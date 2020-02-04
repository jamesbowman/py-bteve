import time
import gameduino as GD
import math
import random

def blinka(eve):
    eve.BitmapHandle(0)
    eve.cmd_loadimage(0, 0)
    eve.load(open("circuitpython.png", "rb"))

    eve.BitmapHandle(1)
    eve.cmd_loadimage(-1, 0)
    eve.load(open("blinka100.png", "rb"))
    eve.BitmapSize(GD.BILINEAR, GD.BORDER, GD.BORDER, 100, 100)

    r = 100                                 # radius for circle of Blinkas

    for t in range(0, 3600, 2):
        eve.Clear(1,1,1)
        eve.Begin(GD.BITMAPS)
        eve.BitmapHandle(0)                 # Draw the background
        eve.Vertex2f(0, 0)

        eve.BitmapHandle(1)                 # Ten Blinkas, 36 degrees apart
        N = 10
        for i in range(N):
            angle = 360 * i / N + t
            eve.cmd_loadidentity()
            eve.cmd_rotatearound(50, 50, angle)
            eve.cmd_setmatrix()
            th = math.radians(-angle)
            x = r * math.sin(th)
            y = r * math.cos(th)
            eve.Vertex2f(240 - 50 + x, 136 - 50 + y)
        eve.swap()

def fizz(eve):
    rr = random.randrange
    while True:
        eve.Clear(1, 1, 1)
        eve.Begin(GD.POINTS)
        # random.seed(7)
        # eve.finish()

        t0 = eve.rd32(GD.REG_CLOCK)
        for i in range(100):
            eve.ColorRGB(rr(256), rr(256), rr(256))
            eve.PointSize(100 + rr(900))
            eve.Vertex2f(rr(480), rr(272))

        t1 = eve.rd32(GD.REG_CLOCK)
        print('took', 1000 * (0xffffffff & (t1 - t0)) / 60e6, 'ms')
        eve.swap()

from gameduino_circuitpython import GameduinoCircuitPython
eve = GameduinoCircuitPython()
eve.init()
fizz(eve)
