import sys
import bteve as eve
import board
import busio

if sys.implementation.name == "circuitpython":
    gd = eve.Gameduino()
else:
    from spidriver import SPIDriver
    gd = eve.Gameduino(SPIDriver(sys.argv[1]))
gd.init()

i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass

def pot(a):
    result = bytearray(1)
    i2c.writeto_then_readfrom(a, bytes([0xff]), result)
    return result[0]

while True:
    gd.finish()
    (r, g, b) = (pot(0x2a),pot(0x28), pot(0x2c))
    gd.ClearColorRGB(r, g, b)
    gd.Clear()
    def gauge(x, bg, c):
        gd.cmd_bgcolor(bg)
        gd.cmd_gauge(x, 90, 80, eve.OPT_FLAT, 4, 2, c, 255)
        gd.cmd_number(x, 150, 29, eve.OPT_CENTER, c)

    gauge(440, 0x401010, r)
    gauge(640, 0x104010, g)
    gauge(840, 0x101040, b)
    gd.swap()
