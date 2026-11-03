import sys
import bteve as eve

if sys.implementation.name == "circuitpython":
    gd = eve.Gameduino()
else:
    from spidriver import SPIDriver
    gd = eve.Gameduino(SPIDriver(sys.argv[1]))
gd.init()

gd.ClearColorRGB(0x20, 0x40, 0x20)
gd.Clear()
gd.cmd_text(gd.w // 2, gd.h // 2, 31, eve.OPT_CENTER, "Hello world")
gd.swap()
