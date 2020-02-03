import time
if 1:
    from gameduino_circuitpython import GameduinoCircuitPython
    eve = GameduinoCircuitPython()
else:
    from gameduino_spidriver import GameduinoSPIDriver
    eve = GameduinoSPIDriver()
eve.init()

POINTS               = 2

def T():
    return time.monotonic()
    return time.ticks_us() / 1e6

eve.ClearColorRGB(0x20, 0x20, 0x40)
eve.Clear(1,1,1)
eve.ColorRGB(255, 50, 50)
eve.Begin(POINTS)
eve.PointSize(64)
eve.finish()
t0 = T()
for i in range(1000):
    # eve.Vertex2f(i, i)
    eve.cmd_append(0x120, 0)
eve.flush()
t1 = T()
print(t1 - t0)
eve.ColorRGB(255, 255, 255)
msg = "1000 points took %.1f ms" % ((t1 - t0) * 1000)
eve.cmd_text(220, 133, 28, 0, msg)
print(msg)
eve.swap()
