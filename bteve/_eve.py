import struct

class _EVE:

    model = 0

    def setmodel(self, x):
        self.model = x

    def cc(self, s):
        assert (len(s) % 4) == 0
        self.__buf += s
        while len(self.__buf) > 512:
            self.write(self.__buf[:512])
            self.__buf = self.__buf[512:]

    def register(self, sub):
        self.__buf = b''
        getattr(sub, 'write') # Confirm that there is a write method

    def flush(self):
        self.write(self.__buf)
        self.__buf = b''

    def c4(self, i):
        """Send a 32-bit value to the GD2."""
        self.cc(struct.pack("I", i))

    def cmd0(self, num):
        self.c4(0xffffff00 | num)

    def cmd(self, num, fmt, args):
        self.c4(0xffffff00 | num)
        self.cc(struct.pack(fmt, *args))


    # The basic graphics instructions

    def AlphaFunc(self, func, ref):
        self.c4((9 << 24) | ((func & 7) << 8) | ((ref & 255)))
    def Begin(self, prim):
        self.c4((31 << 24) | ((prim & 15)))
    def BitmapHandle(self, handle):
        self.c4((5 << 24) | ((handle & 31)))
    def BitmapLayout(self, format, linestride, height):
        self.c4((7 << 24) | ((format & 31) << 19) | ((linestride & 1023) << 9) | ((height & 511)))
    def BitmapSize(self, filter, wrapx, wrapy, width, height):
        self.c4((8 << 24) | ((filter & 1) << 20) | ((wrapx & 1) << 19) | ((wrapy & 1) << 18) | ((width & 511) << 9) | ((height & 511)))
    def BitmapSource(self, addr):
        self.c4((1 << 24) | ((addr & 0xffffff)))

    def _transform(self, opcode, args):
        """ Handle the dual-format fixed-point 8.8 / 1.15 
            used by BitmapTransformA,B,D,E opcodes """
        if self.model == 0:
            (p, a) = args
        else:
            (v, ) = args
            if -2 <= v < 2:
                (p, a) = (1, int(32768 * v))
            else:
                (p, a) = (0, int(256 * v))
            self.c4((opcode << 24) | ((p & 1) << 17) | (a & 131071))

    def BitmapTransformA(self, *args):
        self._transform(21, args)
    def BitmapTransformB(self, *args):
        self._transform(22, args)
    def BitmapTransformD(self, *args):
        self._transform(24, args)
    def BitmapTransformE(self, *args):
        self._transform(25, args)

    def BitmapTransformC(self, c):
        if self.model == 0:
            x = c
        else:
            x = int(256 * c)
        self.c4((23 << 24) | (x & 16777215))
    def BitmapTransformF(self, f):
        if self.model == 0:
            x = f
        else:
            x = int(256 * f)
        self.c4((26 << 24) | (x & 16777215))

    def BlendFunc(self, src, dst):
        self.c4((11 << 24) | ((src & 7) << 3) | ((dst & 7)))
    def Call(self, dest):
        self.c4((29 << 24) | ((dest & 65535)))
    def Cell(self, cell):
        self.c4((6 << 24) | ((cell & 127)))
    def ClearColorA(self, alpha):
        self.c4((15 << 24) | ((alpha & 255)))
    def ClearColorRGB(self, red, green, blue):
        self.c4((2 << 24) | ((red & 255) << 16) | ((green & 255) << 8) | ((blue & 255)))
    def Clear(self, c = 1, s = 1, t = 1):
        self.c4((38 << 24) | ((c & 1) << 2) | ((s & 1) << 1) | ((t & 1)))
    def ClearStencil(self, s):
        self.c4((17 << 24) | ((s & 255)))
    def ClearTag(self, s):
        self.c4((18 << 24) | ((s & 255)))
    def ColorA(self, alpha):
        self.c4((16 << 24) | ((alpha & 255)))
    def ColorMask(self, r, g, b, a):
        self.c4((32 << 24) | ((r & 1) << 3) | ((g & 1) << 2) | ((b & 1) << 1) | ((a & 1)))
    def ColorRGB(self, red, green, blue):
        self.c4((4 << 24) | ((red & 255) << 16) | ((green & 255) << 8) | ((blue & 255)))
    def Display(self):
        self.c4((0 << 24))
    def End(self):
        self.c4((33 << 24))
    def Jump(self, dest):
        self.c4((30 << 24) | ((dest & 65535)))
    def LineWidth(self, width):
        self.c4((14 << 24) | ((int(8 * width) & 4095)))
    def Macro(self, m):
        self.c4((37 << 24) | ((m & 1)))
    def PointSize(self, size):
        self.c4((13 << 24) | ((int(8 * size) & 8191)))
    def RestoreContext(self):
        self.c4((35 << 24))
    def Return(self):
        self.c4((36 << 24))
    def SaveContext(self):
        self.c4((34 << 24))

    def ScissorSize(self, width, height):
        self.c4((28 << 24) | ((width & 4095) << 12) | ((height & 4095)))
    def ScissorXY(self, x, y):
        self.c4((27 << 24) | ((x & 2047) << 11) | ((y & 2047)))

    def StencilFunc(self, func, ref, mask):
        self.c4((10 << 24) | ((func & 7) << 16) | ((ref & 255) << 8) | ((mask & 255)))
    def StencilMask(self, mask):
        self.c4((19 << 24) | ((mask & 255)))
    def StencilOp(self, sfail, spass):
        self.c4((12 << 24) | ((sfail & 7) << 3) | ((spass & 7)))
    def TagMask(self, mask):
        self.c4((20 << 24) | ((mask & 1)))
    def Tag(self, s):
        self.c4((3 << 24) | ((s & 255)))

    _scale = 16

    def VertexFormat(self, frac):
        self.c4((39 << 24) | (frac & 7))
        self._scale = 1 << frac

    def Vertex2f(self, x, y):
        if hasattr(x, '__iter__') and hasattr(y, '__iter__'):
            for (xi, yi) in zip(x, y):
                self.Vertex2f(xi, yi)
            return
        x = int(self._scale * x)
        y = int(self._scale * y)
        self.c4(0x40000000 | ((x & 32767) << 15) | (y & 32767))

    def Vertex2ii(self, x, y, handle = 0, cell = 0):
        self.c4((2 << 30) | ((x & 511) << 21) | ((y & 511) << 12) | ((handle & 31) << 7) | ((cell & 127)))

    def BitmapLayoutH(self, linestride, height):
        self.c4((40 << 24) | (((linestride) & 3) << 2) | (((height) & 3)))

    def BitmapSizeH(self, width, height):
        self.c4((41 << 24) | (((width) & 3) << 2) | (((height) & 3)))

    def PaletteSource(self, addr):
        self.c4((42 << 24) | (((addr) & 4194303)))

    def VertexTranslateX(self, x):
        self.c4((43 << 24) | (((int(16 * x)) & 131071)))

    def VertexTranslateY(self, y):
        self.c4((44 << 24) | (((int(16 * y)) & 131071)))

    def Nop(self):
        self.c4((45 << 24))

    def BitmapExtFormat(self, fmt):
        self.c4((46 << 24) | (fmt & 65535))

    def BitmapSwizzle(self, r, g, b, a):
        self.c4((47 << 24) | ((r & 7) << 9) | ((g & 7) << 6) | ((b & 7) << 3) | ((a & 7)))
