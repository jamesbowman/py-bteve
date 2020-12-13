import sys
import random
import bteve as eve

import game

PADDLE_SIZE = 45

def draw_court(gd):
    gd.ClearColorRGB(0, 10, 0)
    gd.Clear()
    gd.LineWidth(10)
    gd.PointSize(10)
    gd.Begin(eve.LINES)
    for y in (5, 720 - 5):
        gd.Vertex2f(40, y)
        gd.Vertex2f(1240, y)
    gd.Begin(eve.POINTS)
    for y in range(20, 710, 20):
        gd.Vertex2f(640, y)

def sfx(gd, inst, midi = 0):
    gd.cmd_regwrite(eve.REG_SOUND, inst + (midi << 8))
    gd.cmd_regwrite(eve.REG_PLAY, 1)
    gd.flush()

class Ball:
    def __init__(self, gd):
        self.gd = gd
        self.pos = game.Point(320, 360)
        self.vel = game.Point(7, 8)
        self.hide()

    def hide(self):
        self.servetimer = 60

    def move(self, py):
        if self.servetimer != 0:
            self.servetimer -= 1
            if self.servetimer == 0:
                sfx(gd, 0x18, 68)
            return (0, 0)
        n = self.pos + self.vel

        edge_l = (self.vel.x < 0) and (30 < n.x < 45)
        edge_r = (self.vel.x > 0) and (1225 < n.x < 1235)
        if (edge_l or edge_r) and abs(n.y - py[edge_r]) < PADDLE_SIZE:
            self.vel.x *= -1
            self.vel.y += random.randrange(-1, 2)
            sfx(gd, 0x10, 62)
        if not (10 < n.y < 710):
            self.vel.y *= -1
            sfx(gd, 0x10, 63)
        self.pos = n
        if not (0 < self.pos.x < 1280):
            self.pos.x -= (30 * self.vel.x)
            self.vel.x *= -1
            self.vel.y = random.randrange(-7, 8)
            self.hide()
            sfx(gd, 0x18, 40)
            if self.vel.x < 0:
                return (0, 1)
            else:
                return (1, 0)
        return (0, 0)

    def draw(self):
        gd = self.gd
        if self.servetimer == 0:
            gd.PointSize(16)
            gd.Begin(eve.POINTS)
            self.pos.draw(gd)

class Scores:
    def __init__(self):
        self.s = [0, 0]

    def update(self, ch):
        self.s[0] += ch[0]
        self.s[1] += ch[1]

    def draw(self, gd):
        for (x, s) in zip((640 - 100, 640 + 100), self.s):
            gd.cmd_number(x, 80, 31, eve.OPT_CENTER, s)

def pong(gd):
    gd.init()
    gd.cmd_romfont(31, 34)

    ball = Ball(gd)
    scores = Scores()

    def control(c, y):
        y -= (c["ry"] - 16)
        return max(45, min(y, 675))
    yy = [360, 360]
    while 1:
        gd.finish()
        cc = gd.controllers()
        if cc[0]['bh'] or cc[1]['bh']:
            return
        yy = [control(c, y) for (c, y) in zip(cc, yy)]
        scores.update(ball.move(yy))

        gd.VertexFormat(3)

        draw_court(gd)

        gd.LineWidth(20)
        for x,y in [(40, yy[0]), (1240, yy[1])]:
            gd.Begin(eve.LINES)
            gd.Vertex2f(x, y - PADDLE_SIZE)
            gd.Vertex2f(x, y + PADDLE_SIZE)
        ball.draw()
        scores.draw(gd)
        gd.swap()

if sys.implementation.name == 'circuitpython':
    gd = eve.Gameduino()
else:
    from spidriver import SPIDriver
    gd = eve.GameduinoSPIDriver(SPIDriver(sys.argv[1]))
pong(gd)
