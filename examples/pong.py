import random
from gameduino_spidriver import GameduinoSPIDriver
import registers as gd3

PADDLE_SIZE = 45

def draw_court(gd):
    gd.ClearColorRGB(0, 10, 0)
    gd.Clear()
    gd.LineWidth(16 * 5)
    gd.PointSize(16 * 5)
    gd.Begin(gd3.LINES)
    for y in (5, 720 - 5):
        gd.Vertex2f(40, y)
        gd.Vertex2f(1240, y)
    gd.Begin(gd3.POINTS)
    for y in range(20, 710, 20):
        gd.Vertex2f(640, y)

class Ball:
    def __init__(self):
        self.x = 320
        self.y = 360
        self.xv = 7
        self.yv = 8
        self.hide()

    def hide(self):
        self.servetimer = 60

    def move(self, py):
        if self.servetimer != 0:
            self.servetimer -= 1
            return (0, 0)
        x = self.x + self.xv
        y = self.y + self.yv
        if (self.xv < 0) and (30 < x < 45) and abs(y - py[0]) < PADDLE_SIZE:
            self.xv *= -1
            self.yv += random.randrange(-1, 2)
        if (self.xv > 0) and (1225 < x < 1235) and abs(y - py[1]) < PADDLE_SIZE:
            self.xv *= -1
            self.yv += random.randrange(-1, 2)
        if not (10 < y < 710):
            self.yv *= -1
        (self.x, self.y) = (x, y)
        if not (0 < x < 1280):
            self.x -= (30 * self.xv)
            self.xv *= -1
            self.yv = random.randrange(-7, 8)
            self.hide()
            if x < 0:
                return (0, 1)
            else:
                return (1, 0)
        return (0, 0)

    def draw(self, gd):
        if self.servetimer == 0:
            gd.PointSize(16 * 10)
            gd.Begin(gd3.POINTS)
            gd.Vertex2f(self.x, self.y)

class Scores:
    def __init__(self):
        self.s = [0, 0]

    def update(self, ch):
        self.s[0] += ch[0]
        self.s[1] += ch[1]

    def draw(self, gd):
        for (x, s) in zip((640 - 100, 640 + 100), self.s):
            gd.cmd_number(x, 80, 31, gd3.OPT_CENTER, s)

if __name__ == "__main__":
    gd = GameduinoSPIDriver()
    gd.init()
    gd.cmd_romfont(31, 34)

    ball = Ball()
    scores = Scores()

    def control(c, y):
        y -= (c["ry"] - 16)
        return max(45, min(y, 675))
    yy = [360, 360]
    while 1:
        gd.finish()
        cc = gd.controllers()
        yy = [control(c, y) for (c, y) in zip(cc, yy)]
        scores.update(ball.move(yy))

        gd.VertexFormat(3)

        draw_court(gd)

        gd.LineWidth(16 * 10)
        for x,y in [(40, yy[0]), (1240, yy[1])]:
            gd.Begin(gd3.LINES)
            gd.Vertex2f(x, y - PADDLE_SIZE)
            gd.Vertex2f(x, y + PADDLE_SIZE)
        ball.draw(gd)
        scores.draw(gd)
        gd.swap()
