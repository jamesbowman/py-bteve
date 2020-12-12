import sys
import random
import time
import bteve as eve
import game

rnd = random.randrange

def run(L):
    matches = [L[i]==L[i+1]==L[i+2] for i in range(6)]
    if not True in matches:
        return None
    matches += [False]
    a = matches.index(True)
    b = a + matches[a:].index(False) + 2
    return range(a, b)

class FieldPoint(game.Point):
    def __add__(self, other):
        r = FieldPoint(self.x + other.x, self.y + other.y)
        r.x %= 8
        r.y %= 8
        return r
    def project(self):
        return game.Point(320 + 80 * self.x, 40 + 80 * self.y)

class FruitGame:
    def __init__(self, gd):
        gd.cmd_loadimage(0, 0)
        fn = "fruit.png"
        with open(fn, "rb") as f:
            gd.load(f)
        gd.cmd_setbitmap(0, eve.ARGB4, 80, 80)

        gd.cmd_romfont(31, 34)

        random.seed(2)
        sels = [(0,1), (2,3,4)]
        self.board = [
            [random.choice(sels[1 & (x ^ y)]) for y in range(8)]
            for x in range(8)
        ]

        self.still = [0 for i in range(8)]
        self.gd = gd
        self.cursor = FieldPoint(0,0)
        self.prev_press = False
        self.reset()

    def reset(self):
        self.score = 0
        self.scoret = 0
        self.time = 45

    def draw(self, bar = None, fall = 0):
        gd = self.gd
        gd.cmd_gradient(0, 0, 0x202040, 0, 720, 0xffd0c0)
        gd.SaveContext()
        gd.ColorRGB(0, 0, 0)

        self.score += (self.score != self.scoret)
        gd.cmd_number(160, 360, 31, eve.OPT_CENTER | 4, self.score)
        t = int(self.time)
        gd.cmd_clock(1120,  360, 100,
                     eve.OPT_FLAT | eve.OPT_NOHM | eve.OPT_NOBACK,
                     0, 0, int(self.time), int(1000 * (self.time - t)))

        gd.RestoreContext()

        if bar is not None:
            gd.Begin(eve.LINES)
            gd.LineWidth(8 * 80)
            for (x, y) in bar:
                gd.Vertex2f(360 + 80 * x, 80 + 80 * y)

        if bar is None and fall == 0:
            p0 = self.cursor.project()
            p1 = p0 + game.Point(80, 80)
            gd.SaveContext()
            gd.ColorA(128)
            gd.Begin(eve.RECTS)
            gd.LineWidth(60)
            p0.draw(gd)
            p1.draw(gd)
            gd.RestoreContext()

        gd.Begin(eve.BITMAPS)
        for x in range(8):
            for y in range(0, 8):
                gd.Cell(self.board[x][y])
                p = FieldPoint(x, y)
                o = game.Point(0, fall * (y < self.still[x]))
                (p.project() - o).draw(gd)

        gd.swap()

    def match(self):
        b = self.board
        for x in range(8):
            r = run(b[x])
            if r is not None:
                self.scoret += len(r) * 7
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
                self.scoret += len(r) * 7
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

    def ui(self):
        gd.finish()
        c = gd.controllers()[0]
        anypress = any(c[b] for b in ['bdl', 'bdr', 'bdu', 'bdd', 'ba', 'bb', 'bx', 'by'])
        press = anypress and not self.prev_press
        self.prev_press = anypress

        dir = game.Point(-c['bdl'] + c['bdr'], -c['bdu'] + c['bdd'])
        if press:
            self.cursor += dir

        def exchange(dx, dy):
            p0 = self.cursor
            p1 = self.cursor + game.Point(dx, dy)
            (self.board[p0.x][p0.y], self.board[p1.x][p1.y]) = (self.board[p1.x][p1.y], self.board[p0.x][p0.y])
        if press:
            if c['ba']:
                exchange(1, 0)
            if c['by']:
                exchange(-1, 0)
            if c['bx']:
                exchange(0, -1)
            if c['bb']:
                exchange(0, 1)

    def play(self):
        self.draw()
        t0 = time.time()
        while 1:
            self.ui()
            self.draw()
            t1 = time.time()
            self.time = max(0, self.time - (t1 - t0))
            t0 = t1
            self.match()
            t0 = time.time()

if sys.implementation.name == 'circuitpython':
    gd = eve.Gameduino()
else:
    from spidriver import SPIDriver
    gd = eve.GameduinoSPIDriver(SPIDriver(sys.argv[1]))
gd.init()

FruitGame(gd).play()
