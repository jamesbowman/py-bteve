import random
import time

import bteve as eve

gd = eve.Gameduino()
gd.init()

def run(L):
    matches = [L[i]==L[i+1]==L[i+2] for i in range(6)]
    if not True in matches:
        return None
    matches += [False]
    a = matches.index(True)
    b = a + matches[a:].index(False) + 2
    return range(a, b)

class FruitGame:
    def __init__(self):
        gd.cmd_loadimage(0, 0)
        fn = "fruit.png"
        with open(fn, "rb") as f:
            gd.load(f)
        gd.cmd_setbitmap(0, eve.ARGB4, 80, 80)

        random.seed(0)
        self.board = [
            [random.randrange(5) for y in range(8)]
            for x in range(8)
        ]
        if 0:
            self.board[5][2] = 1
            self.board[5][3] = 1
            self.board[5][4] = 1
            self.board[5][5] = 1

        self.still = [0 for i in range(8)]

    def collapse(self):
        b = self.board
        for x in range(8):
            r = run(b[x])
            if r is not None:
                for i in range(60):
                    self.draw(bar = ((x, r.start), (x, r.stop - 1)))
                self.still[x] = r.stop
                b[x] = [random.randrange(5) for i in r] + b[x][:r.start] + b[x][r.stop:]
                for i in range(80 * len(r), -1, -10):
                    self.draw(fall = i)
                self.still[x] = 0
                return
        
    def draw(self, bar = None, fall = 0):
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
        gd.swap()

        while 0:
            print(gd.controllers()[0])

    def play(self):
        self.draw()
        while 1:
            self.collapse()
            self.draw()
            if random.randrange(2) == 0:
                self.board[random.randrange(8)][random.randrange(8)] = random.randrange(5)


FruitGame().play()
