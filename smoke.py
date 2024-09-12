import sys
import array
import time
import bteve as eve

try:
    import numpy as np
except ImportError:
    import ulab.numpy as np

def assert_same(s):
    assert len(set(s)) == 1

def assert_unique(s):
    assert len(set(s)) == len(s)

class EveCapture(eve.EVE):
    def __init__(self):
        self.buf = []

    def write(self, bb):
        self.buf.append(bytes(bb))

    def collect(self, verbose = False):
        self.flush()
        r = list(array.array("I", b''.join(self.buf)))
        self.buf = []
        if verbose:
            for x in r:
                print(f"{x:08x}")
        return r

gd = EveCapture()
gd.register(gd)
gd.setmodel(817)

def combos(n):
    if n == 0:
        yield ()
    else:
        for c in combos(n - 1):
            yield c + (0, )
            yield c + (1, )

def diff(actual, expect):
    assert len(actual) == len(expect), "Actual and expect must have same length"
    for i in range(len(actual)):
        if actual[i] != expect[i]:
            print(f"Mismatch at {i} / {len(expect)}")
            print(f"  actual @ {i}: {actual[i]} {actual[i]:#x}")
            print(f"expected @ {i}: {expect[i]} {expect[i]:#x}")
            return

def test_opcodes():

    methods = (
        (0, (
            gd.Display,
            gd.End,
            gd.RestoreContext,
            gd.Return,
            gd.SaveContext,
            gd.Nop,
        )),
        (1, (
            gd.BitmapTransformA,
            gd.BitmapTransformB,
            gd.BitmapTransformC,
            gd.BitmapTransformD,
            gd.BitmapTransformE,
            gd.BitmapTransformF,
            gd.Begin,
            gd.BitmapHandle,
            gd.BitmapSource,
            gd.Call,
            gd.Cell,
            gd.ClearColorA,
            gd.ClearStencil,
            gd.ClearTag,
            gd.ColorA,
            gd.TagMask,
            gd.Tag,
            gd.VertexTranslateX,
            gd.VertexTranslateY,
            gd.Jump,
            gd.LineWidth,
            gd.Macro,
            gd.PointSize,
            gd.StencilMask,
            gd.VertexFormat,
            gd.PaletteSource,
            gd.BitmapExtFormat,
        )),
        (2, (
            gd.AlphaFunc,
            gd.BlendFunc,
            gd.ScissorXY,
            gd.StencilOp,
            gd.Vertex2f,
            gd.BitmapSizeH,
            gd.ScissorSize,
            gd.BitmapLayoutH,
        )),
        (3, (
            gd.BitmapLayout,
            gd.ClearColorRGB,
            gd.Clear,
            gd.ColorRGB,
            gd.StencilFunc,
        )),
        (4, (
            gd.ColorMask,
            gd.Vertex2ii,
            gd.BitmapSwizzle,
        )),
        (5, (
            gd.BitmapSize,
        )),
    )

    for (arity, meths) in methods:
        for m in meths:
            for a in combos(arity):
                m(*a)

    gd.flush()

    actual = gd.collect()
    assert len(set(actual)) == len(actual), "Not all opcodes are unique"

    expected = [
0x00000000, 
0x21000000, 
0x23000000, 
0x24000000, 
0x22000000, 
0x2d000000, 
0x15020000, 0x15028000,
0x16020000, 0x16028000,
0x17000000, 0x17000100, 
0x18020000, 0x18028000,
0x19020000, 0x19028000,
0x1a000000, 0x1a000100, 
0x1f000000, 0x1f000001, 
0x05000000, 0x05000001, 
0x01000000, 0x01000001, 
0x1d000000, 0x1d000001, 
0x06000000, 0x06000001, 
0x0f000000, 0x0f000001, 
0x11000000, 0x11000001, 
0x12000000, 0x12000001, 
0x10000000, 0x10000001, 
0x14000000, 0x14000001, 
0x03000000, 0x03000001, 
0x2b000000, 0x2b000010, 
0x2c000000, 0x2c000010, 
0x1e000000, 0x1e000001, 
0x0e000000, 0x0e000008, 
0x25000000, 0x25000001, 
0x0d000000, 0x0d000008, 
0x13000000, 0x13000001, 
0x27000000, 0x27000001, 
0x2a000000, 0x2a000001, 
0x2e000000, 0x2e000001, 
0x09000000, 0x09000001, 0x09000100, 0x09000101, 
0x0b000000, 0x0b000001, 0x0b000008, 0x0b000009, 
0x1b000000, 0x1b000001, 0x1b000800, 0x1b000801, 
0x0c000000, 0x0c000001, 0x0c000008, 0x0c000009, 
0x40000000, 0x40000002, 0x40010000, 0x40010002, 
0x29000000, 0x29000001, 0x29000004, 0x29000005, 
0x1c000000, 0x1c000001, 0x1c001000, 0x1c001001, 
0x28000000, 0x28000001, 0x28000004, 0x28000005, 
0x07000000, 0x07000001, 0x07000200, 0x07000201, 0x07080000, 0x07080001, 0x07080200, 0x07080201, 
0x02000000, 0x02000001, 0x02000100, 0x02000101, 0x02010000, 0x02010001, 0x02010100, 0x02010101, 
0x26000000, 0x26000001, 0x26000002, 0x26000003, 0x26000004, 0x26000005, 0x26000006, 0x26000007, 
0x04000000, 0x04000001, 0x04000100, 0x04000101, 0x04010000, 0x04010001, 0x04010100, 0x04010101, 
0x0a000000, 0x0a000001, 0x0a000100, 0x0a000101, 0x0a010000, 0x0a010001, 0x0a010100, 0x0a010101, 
0x20000000, 0x20000001, 0x20000002, 0x20000003, 0x20000004, 0x20000005, 0x20000006, 0x20000007, 0x20000008, 0x20000009, 0x2000000a, 0x2000000b, 0x2000000c, 0x2000000d, 0x2000000e, 0x2000000f, 
0x80000000, 0x80000001, 0x80000080, 0x80000081, 0x80001000, 0x80001001, 0x80001080, 0x80001081, 0x80200000, 0x80200001, 0x80200080, 0x80200081, 0x80201000, 0x80201001, 0x80201080, 0x80201081, 
0x2f000000, 0x2f000001, 0x2f000008, 0x2f000009, 0x2f000040, 0x2f000041, 0x2f000048, 0x2f000049, 0x2f000200, 0x2f000201, 0x2f000208, 0x2f000209, 0x2f000240, 0x2f000241, 0x2f000248, 0x2f000249, 
0x08000000, 0x08000001, 0x08000200, 0x08000201, 0x08040000, 0x08040001, 0x08040200, 0x08040201, 0x08080000, 0x08080001, 0x08080200, 0x08080201, 0x080c0000, 0x080c0001, 0x080c0200, 0x080c0201, 0x08100000, 0x08100001, 0x08100200, 0x08100201, 0x08140000, 0x08140001, 0x08140200, 0x08140201, 0x08180000, 0x08180001, 0x08180200, 0x08180201, 0x081c0000, 0x081c0001, 0x081c0200, 0x081c0201,
    ]
    if 0:
        print("[")
        prev = -1
        for i,e in enumerate(actual):
            if (prev >> 24) != (e >> 24):
                print()
            print(f"0x{e:08x}, ", end = "")
            prev = e
        print("]")
    if actual != expected:
        assert False, f"{diff(actual, expected)}"
    print("test_opcodes(): passed")

def test_numpy():
    xx = np.array([1, 3.1, 0])
    yy = np.array([2, 4.9, 0])

    # Run it the scalar way, for reference
    for (x, y) in zip(xx, yy):
        gd.Vertex2f(x, y)
    out_scalar = gd.collect()

    # Run it using arrays
    gd.Vertex2f(xx, yy)
    out_array = gd.collect()

    # for e in out_array: print(f"0x{e:08x}")
    assert out_scalar == out_array, f"{foo}"
    print("test_numpy(): passed")

def test_numpy_perf():
    N = 1000
    xx = np.zeros(N)
    yy = np.zeros(N)
    t0 = time.monotonic()
    gd.Vertex2f(xx, yy)
    t1 = time.monotonic()
    t = t1 - t0
    rate = N / t
    print("test_numpy_perf(): passed")
    print(f"   [ {rate:.0f} vertices/s ]")
    gd.collect()

def test_transform():
    for meth in (gd.BitmapTransformA, gd.BitmapTransformB, gd.BitmapTransformD, gd.BitmapTransformE):
        gd.setmodel(0)
        meth(0, 0x500)
        gd.setmodel(817)
        meth(5.0)
        assert_same(gd.collect())
    for meth in (gd.BitmapTransformC, gd.BitmapTransformF):
        gd.setmodel(0)
        meth(0x900)
        gd.setmodel(817)
        meth(9.0)
        assert_same(gd.collect())
    print("test_transform(): passed")

def test_820_opcodes():
    if eve.__arch__ == "82x":
        mx = 0xffffffff
        gd.ClearTag(mx)
        gd.Tag(mx)
        gd.PaletteSource(mx)
        gd.PaletteSourceH(mx)
        gd.BitmapHandle(mx)
        gd.BitmapSource(mx)
        gd.BitmapSourceH(mx)
        expected = [
            0x12ffffff,
            0x03ffffff,
            0x2affffff,
            0x320000ff,
            0x0500003f,
            0x01ffffff,
            0x310000ff,
        ]
        actual = gd.collect()
        if actual != expected:
            assert False, f"{diff(actual, expected)}"
        print("test_820_opcodes(): passed")

def test_vertex_precision():
    for p in (0, 1, 2, 3, 4):
        gd.VertexFormat(p)
        gd.Vertex2f(5, 5)
    assert_unique(gd.collect())

if not ('pytest' in sys.modules):
    print("-------------------- STARTED --------------------")
    test_opcodes()
    test_numpy()
    test_transform()
    test_numpy_perf()
    test_820_opcodes()
    print("test complete")
