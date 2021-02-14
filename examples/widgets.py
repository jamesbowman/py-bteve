import sys
import bteve as eve
import struct

def widgets(gd):
    TAG_DIAL      = 200
    TAG_SLIDER    = 201
    TAG_TOGGLE    = 202
    TAG_BUTTON1   = 203
    TAG_BUTTON2   = 204

    value = 15000
    message = 40 * ' '
    options = eve.OPT_FLAT
    prevkey = 0

    def xf(c):
        return c * gd.w // 480
    def vx(x, y):
        gd.Vertex2f(xf(x), xf(y))

    key = 0
    while True:
        gd.get_inputs()
        if gd.inputs.tracker.tag in (TAG_DIAL, TAG_SLIDER, TAG_TOGGLE):
            value = gd.inputs.tracker.val
        tag = gd.inputs.touch.tag
        if tag == TAG_BUTTON1:
            options = eve.OPT_FLAT
        elif tag == TAG_BUTTON2:
            options = 0
        else:
            key = tag
        if (prevkey == 0x00) and (ord(' ') <= key < 0x7f):
            message = message[1:] + chr(key)
        prevkey = key

        gd.cmd_gradient(0, 0,   0x404044, xf(480), xf(480), 0x606068)
        gd.ColorRGB(0x70, 0x70, 0x70)

        gd.LineWidth(xf(8))
        gd.Begin(eve.RECTS)

        vx(8, 8)
        vx(128, 128)

        vx(8, 136 + 8)
        vx(128, 136 + 128)

        vx(144, 136 + 8)
        vx(472, 136 + 128)
        gd.ColorRGB(255, 255, 255)

        gd.Tag(TAG_DIAL)
        gd.cmd_dial(xf(68), xf(68), xf(50), options, 360 * value / 65536)
        gd.cmd_track(xf(68), xf(68), 1, 1, TAG_DIAL)

        gd.Tag(TAG_SLIDER)
        gd.cmd_slider(xf(16), xf(199), xf(104), xf(10), options, value, 65535)
        gd.cmd_track(xf(16), xf(199), xf(104), xf(10), TAG_SLIDER)

        gd.Tag(TAG_TOGGLE)
        gd.cmd_toggle(xf(360), xf(62), xf(80), 29, options, value, "that", "this")
        gd.cmd_track(xf(360), xf(62), xf(80), xf(20), TAG_TOGGLE)

        gd.Tag(255)
        gd.cmd_number(xf(68), xf(136), 30, eve.OPT_CENTER | 5, value)

        gd.cmd_clock(xf(184), xf(48), xf(40), options | eve.OPT_NOSECS, 0, 0, value, 0)
        gd.cmd_gauge(xf(280), xf(48), xf(40), options, 4, 3, value, 65535)

        gd.Tag(TAG_BUTTON1)
        gd.cmd_button(xf(352), xf(12), xf(40), xf(30), 28, options,  "2D")
        gd.Tag(TAG_BUTTON2)
        gd.cmd_button(xf(400), xf(12), xf(40), xf(30), 28, options,  "3D")

        gd.Tag(255)
        gd.cmd_progress(xf(144), xf(100), xf(320), xf(10), options, value, 65535)
        gd.cmd_scrollbar(xf(144), xf(120), xf(320), xf(10), options, value // 2, 32768, 65535)

        gd.cmd_keys(xf(144), xf(168),      xf(320), xf(24), 28, options | eve.OPT_CENTER | key, "qwertyuiop")
        gd.cmd_keys(xf(144), xf(168 + 26), xf(320), xf(24), 28, options | eve.OPT_CENTER | key, "asdfghjkl")
        gd.cmd_keys(xf(144), xf(168 + 52), xf(320), xf(24), 28, options | eve.OPT_CENTER | key, "zxcvbnm,.")
        gd.Tag(ord(' '))
        gd.cmd_button(xf(308 - 60), xf(172 + 74), xf(120), xf(20), 28, options,   "")

        gd.BlendFunc(eve.SRC_ALPHA, eve.ZERO)
        gd.cmd_text(xf((144+472) // 2), xf(146), 18, eve.OPT_CENTERX, message)

        gd.swap()

if sys.implementation.name == "circuitpython":
    gd = eve.Gameduino()
else:
    from spidriver import SPIDriver
    gd = eve.Gameduino(SPIDriver(sys.argv[1]))
gd.init()

widgets(gd)
