import sys
import random
import time
import bteve as eve

rnd = random.randrange

def run(L):
    matches = [L[i]==L[i+1]==L[i+2] for i in range(6)]
    if not True in matches:
        return None
    matches += [False]
    a = matches.index(True)
    b = a + matches[a:].index(False) + 2
    return range(a, b)

class FruitGame:
    def __init__(self, gd):
        gd.cmd_loadimage(0, 0)
        fn = "fruit.png"
        with open(fn, "rb") as f:
            gd.load(f)
        gd.cmd_setbitmap(0, eve.ARGB4, 80, 80)

        random.seed(2)
        sels = [(0,1), (2,3,4)]
        self.board = [
            [random.choice(sels[1 & (x ^ y)]) for y in range(8)]
            for x in range(8)
        ]

        self.still = [0 for i in range(8)]
        self.gd = gd
        self.cursor = (0,0)
        self.prev_press = False

    def match(self):
        b = self.board
        for x in range(8):
            r = run(b[x])
            if r is not None:
                for i in range(30):
                    self.draw(bar = ((x, r.start), (x, r.stop - 1)))
                self.still[x] = r.stop
                b[x] = [rnd(5) for i in r] + b[x][:r.start] + b[x][r.stop:]
                for i in range(80 * len(r), -1, -10):
                    self.draw(fall = i)
                self.still[x] = 0
                return
        b = [[b[j][i] for j in range(8)] for i in range(8)]
        for y in range(8):
            r = run(b[y])
            if r is not None:
                for i in range(30):
                    self.draw(bar = ((r.start, y), (r.stop - 1, y)))
                for x in r:
                    self.still[x] = y + 1
                    self.board[x].pop(y)
                    self.board[x].insert(0, rnd(5))
                for i in range(80, -1, -10):
                    self.draw(fall = i)
                self.still = [0 for i in range(8)]
                return

    def draw(self, bar = None, fall = 0):
        gd = self.gd
        gd.cmd_gradient(0, 0, 0x202040, 0, 720, 0xffd0c0)
        if bar is not None:
            gd.Begin(eve.LINES)
            gd.LineWidth(8 * 80)
            for (x, y) in bar:
                gd.Vertex2f(360 + 80 * x, 80 + 80 * y)

        gd.Begin(eve.BITMAPS)
        for x in range(8):
            for y in range(0, 8):
                gd.Cell(self.board[x][y])
                o = fall * (y < self.still[x])
                gd.Vertex2f(320 + 80 * x, 40 + 80 * y - o)

        if bar is None and fall == 0:
            c = gd.controllers()[0]
            anypress = any(c[b] for b in ['bdl', 'bdr', 'bdu', 'bdd', 'ba', 'bb', 'bx', 'by'])
            press = anypress and not self.prev_press
            self.prev_press = anypress

            cx0 = 320 + 80 * self.cursor[0]
            cy0 = 40 + 80 * self.cursor[1]
            (cx1, cy1) = (cx0 + 80, cy0 + 80)

            gd.Begin(eve.LINE_STRIP)
            gd.LineWidth(32)
            gd.Vertex2f(cx0, cy0)
            gd.Vertex2f(cx1, cy0)
            gd.Vertex2f(cx1, cy1)
            gd.Vertex2f(cx0, cy1)
            gd.Vertex2f(cx0, cy0)

            dir = (-c['bdl'] + c['bdr'], -c['bdu'] + c['bdd'])
            if press:
                self.cursor = ((self.cursor[0] + dir[0]) % 8, (self.cursor[1] + dir[1]) % 8)

            def exchange(dx, dy):
                (i0, j0) = self.cursor
                (i1, j1) = ((self.cursor[0] + dx) % 8, (self.cursor[1] + dy) % 8)
                (self.board[i0][j0], self.board[i1][j1]) = (self.board[i1][j1], self.board[i0][j0])
            if press:
                if c['ba']:
                    exchange(1, 0)
                if c['by']:
                    exchange(-1, 0)
                if c['bx']:
                    exchange(0, -1)
                if c['bb']:
                    exchange(0, 1)

        gd.swap()

    def play(self):
        self.draw()
        while 1:
            self.match()
            self.draw()
            if 0 and rnd(2) == 0:
                self.board[rnd(8)][rnd(8)] = rnd(5)


if sys.implementation.name == 'circuitpython':
    gd = eve.Gameduino()
else:
    from spidriver import SPIDriver
    gd = eve.GameduinoSPIDriver(SPIDriver(sys.argv[1]))
gd.init()
FruitGame(gd).play()
