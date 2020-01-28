import time
import bteve as EVE
import t_micropython

eve = EVE.ConnectedEVE(t_micropython.SPI())
eve.register(eve.write)
eve.standard_startup()

POINTS               = 2

eve.ClearColorRGB(0x20, 0x20, 0x40)
eve.Clear(1,1,1)
eve.ColorRGB(255, 50, 50)
eve.Begin(POINTS)
eve.PointSize(64)
t0 = time.ticks_us()
for i in range(1000):
    eve.Vertex2f(i, i)
eve.flush()
t1 = time.ticks_us()
print(t1 - t0)
eve.swap()
