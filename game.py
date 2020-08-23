import gameduino as GD
import math

class Point:
    def __init__(self, x, y):
        (self.x, self.y) = (x, y)
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    def tuple(self):
        return (self.x, self.y)
    def rotate(self, a):
        ar = math.radians(a)
        s = math.sin(ar)
        c = math.cos(ar)
        return Point((self.x * c) - (self.y * s), (self.x * s) + (self.y * c))

class Sprite:
    def __init__(self, source, fmt, w, h, cells, handle):
        self.source = source
        self.fmt = fmt
        self.w = w
        self.h = h
        self.cells = cells
        self.handle = handle
        self.cx = w / 2
        self.cy = h / 2
        self.anim = None

    def setframes(self, anim):
        self.anim = anim

    def draw(self, eve, x, y, frame = 0, angle = None):
        eve.BitmapHandle(self.handle)
        if self.anim is None:
            eve.Cell(frame % self.cells)
        else:
            eve.Cell(self.anim[frame % len(self.anim)])
        if angle is None:
            eve.Vertex2f(x - self.cx, y - self.cy)
        else:
            pos = Point(x, y)
            center = Point(self.cx, self.cy)
            corners = [Point(0, 0), Point(self.w, 0), Point(0, self.h), Point(self.w, self.h)]
            tcorners = [(c - center).rotate(angle) + pos for c in corners]
            xx = [p.x for p in tcorners]
            yy = [p.y for p in tcorners]
            p0 = Point(math.floor(min(xx)), math.floor(min(yy)))
            p1 = Point(math.ceil(max(xx)), math.ceil(max(yy)))
            span = p1 - p0
            eve.BitmapSize(GD.BILINEAR, GD.BORDER, GD.BORDER, span.x, span.y)
            pos -= p0

            eve.SaveContext()
            eve.cmd_loadidentity()
            eve.cmd_translate(pos.x, pos.y)
            eve.cmd_rotate(angle)
            eve.cmd_translate(-center.x, -center.y)
            eve.cmd_setmatrix()
            eve.Vertex2f(p0.x, p0.y)
            eve.RestoreContext()
