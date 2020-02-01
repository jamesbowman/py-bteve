import time
from gameduino import Gameduino
import t_micropython

print(879)
eve = Gameduino(t_micropython.SPI())
eve.init()

POINTS               = 2

eve.ClearColorRGB(0x20, 0x20, 0x40)
eve.Clear(1,1,1)
eve.ColorRGB(255, 50, 50)
eve.Begin(POINTS)
eve.PointSize(64)
eve.finish()
t0 = time.ticks_us()
for i in range(1000):
    eve.Vertex2f(i, i)
    # eve.cmd_append(0x120, 0)
eve.flush()
t1 = time.ticks_us()
print(t1 - t0)
eve.ColorRGB(255, 255, 255)
msg = "1000 points took %.1f ms" % ((t1 - t0) / 1000)
eve.cmd_text(220, 133, 28, 0, msg)
print(msg)
eve.swap()
