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
        gd.BitmapHandle(0)
        gd.cmd_loadimage(0, 0)
        fn = "fruit.png"
        with open(fn, "rb") as f:
            gd.load(f)
        gd.cmd_setbitmap(0, eve.ARGB4, 80, 80)

        gd.SaveContext()
        gd.cmd_romfont(31, 34)
        gd.RestoreContext()

        random.seed(2)
        self.initial()

        self.still = [0 for i in range(8)]
        self.gd = gd
        self.prev_press = False
        self.reset()

    def initial(self):
        while True:
            b = [[rnd(5) for y in range(8)] for x in range(8)]
            if any([run(r) for r in b]):
                continue
            b = [[b[j][i] for j in range(8)] for i in range(8)]
            if any([run(r) for r in b]):
                continue
            self.board = b
            break
            
    def reset(self):
        self.score = 0
        self.scoret = 0
        self.time = 0
        self.cursor = FieldPoint(0,0)
        self.cursor2 = None

    def sfx(self, inst, midi = 0):
        gd = self.gd
        gd.cmd_regwrite(eve.REG_SOUND, inst + (midi << 8))
        gd.cmd_regwrite(eve.REG_PLAY, 1)
        gd.flush()

    def draw(self, bar = None, fall = 0, swap = None):
        gd = self.gd
        gd.cmd_gradient(0, 0, 0x202040, 0, 720, 0xffd0c0)

        if bar is not None:
            gd.Begin(eve.LINES)
            gd.LineWidth(80)
            for (x, y) in bar:
                gd.Vertex2f(360 + 80 * x, 80 + 80 * y)

        if bar is None and fall == 0 and swap is None:
            p0 = self.cursor.project()
            p1 = p0 + game.Point(80, 80)
            gd.SaveContext()
            gd.ColorA(128)
            gd.Begin(eve.RECTS)
            gd.LineWidth(8)
            p0.draw(gd)
            p1.draw(gd)
            gd.RestoreContext()

        gd.Begin(eve.BITMAPS)
        
        gd.SaveContext()
        if self.time == 0.0:
            gd.ColorA(128)
        td = {(x, y) for x in range(8) for y in range(8)}
        if swap is not None:
            td -= {self.cursor.tuple(), self.cursor2.tuple()}
        for (x, y) in td:
            gd.Cell(self.board[x][y])
            p = FieldPoint(x, y)
            o = game.Point(0, fall * (y < self.still[x]))
            (p.project() - o).draw(gd)
        if swap is not None:
            (p0, p1) = (self.cursor, self.cursor2)
            (p0p, p1p) = (p0.project(), p1.project())
            d = (p1p - p0p) * swap
            gd.Cell(self.board[p0.x][p0.y])
            (p0p + d).draw(gd)
            gd.Cell(self.board[p1.x][p1.y])
            (p1p - d).draw(gd)
        gd.RestoreContext()

        gd.ColorRGB(0, 0, 0)
        if self.score < self.scoret:
            self.score += 1
            if (self.score % 3) == 0:
                self.sfx(eve.HARP, 80)
        gd.cmd_number(160, 360, 31, eve.OPT_CENTER | 4, self.score)
        t = int(self.time)
        gd.cmd_clock(1120,  360, 100,
                     eve.OPT_FLAT | eve.OPT_NOHM | eve.OPT_NOBACK,
                     0, 0, 0, int(1000 * self.time))
        if self.time == 0.0:
            gd.cmd_text(640, 360, 31, eve.OPT_CENTER, "PRESS START")

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
                return 1
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
                return 1
        return 0

    def exchange(self, dx, dy):
        p0 = self.cursor
        p1 = self.cursor + game.Point(dx, dy)
        self.cursor2 = p1

        def switch():
            for i in range(10):
                self.draw(swap = game.smoothstep(i / 10))
            (self.board[p0.x][p0.y], self.board[p1.x][p1.y]) = (self.board[p1.x][p1.y], self.board[p0.x][p0.y])
        switch()
        self.draw(swap = 0.0)

        if self.match():
            while self.match():
                pass
        else:
            self.sfx(eve.TUBA, 44)
            while True:
                c = gd.controllers()[0]
                if not any(c[b] for b in ['bdl', 'bdr', 'bdu', 'bdd', 'ba', 'bb', 'bx', 'by']):
                    break
            switch()
            self.draw()

    def ui(self):
        c = gd.controllers()[0]
        anypress = any(c[b] for b in ['bdl', 'bdr', 'bdu', 'bdd', 'ba', 'bb', 'bx', 'by'])
        press = anypress and not self.prev_press
        self.prev_press = anypress

        dir = game.Point(-c['bdl'] + c['bdr'], -c['bdu'] + c['bdd'])
        if press:
            self.cursor += dir
            self.sfx(eve.CHACK)

        if press:
            if c['ba']:
                self.exchange(1, 0)
            if c['by']:
                self.exchange(-1, 0)
            if c['bx']:
                self.exchange(0, -1)
            if c['bb']:
                self.exchange(0, 1)

    def play(self):
        while True:
            while gd.controllers()[0]['b+'] == 0:
                self.draw()
            self.initial()
            self.reset()
            self.time = 45

            t0 = time.time()
            while self.time != 0:
                gd.finish()
                self.time = max(0, self.time - (time.time() - t0))
                self.ui()
                t0 = time.time()

                self.draw()
                t0 = time.time()
            self.sfx(eve.ORGAN)

if sys.implementation.name == 'circuitpython':
    gd = eve.Gameduino()
else:
    from spidriver import SPIDriver
    gd = eve.GameduinoSPIDriver(SPIDriver(sys.argv[1]))
gd.init()

FruitGame(gd).play()
