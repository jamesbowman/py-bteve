import bteve as eve
import math

def lerp(t, a, b):
    return a + (b - a) * t
def smoothstep(t):
    return t * t * (3.0 - 2.0 * t)

class Point:
    def __init__(self, x, y):
        (self.x, self.y) = (x, y)
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        return Point(self.x * other, self.y * other)
    def tuple(self):
        return (self.x, self.y)
    def rotate(self, a):
        ar = math.radians(a)
        s = math.sin(ar)
        c = math.cos(ar)
        return Point((self.x * c) - (self.y * s), (self.x * s) + (self.y * c))
    def angle(self):
        return (-90 - math.degrees(math.atan2(self.y, self.x))) % 360
    def draw(self, gd):
        gd.Vertex2f(self.x, self.y)

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

    def draw(self, eve, x, y, frame = 0, angle = 0, xdir = 1):
        eve.BitmapHandle(self.handle)
        if self.anim is None:
            eve.Cell(frame % self.cells)
            eve.Cell(frame % self.cells)
            eve.Cell(frame % self.cells)
            print(frame, self.cells)
        else:
            eve.Cell(self.anim[frame % len(self.anim)])
        if (angle == 0) and (xdir > 0):
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
            eve.BitmapSize(eve.BILINEAR, eve.BORDER, eve.BORDER, span.x, span.y)
            pos -= p0

            eve.SaveContext()
            eve.cmd_loadidentity()
            eve.cmd_translate(pos.x, pos.y)
            if angle:
                eve.cmd_rotate(angle)
            if xdir < 0:
                eve.cmd_scale(-1, 1)
            eve.cmd_translate(-center.x, -center.y)
            eve.cmd_setmatrix()
            eve.Vertex2f(p0.x, p0.y)
            eve.RestoreContext()
