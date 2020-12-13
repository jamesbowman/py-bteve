import sys
import time
import bteve as eve

import game

def temperature(gd, sense):
    gd.init()
    gd.cmd_romfont(16, 33)
    gd.cmd_romfont(17, 34)

    sparkline = []
    t0 = time.time()
    while True:
        # Measure temp continuously until CPU is ready to redraw
        # then compute average

        gd.flush()
        n = 1
        t = sense()
        while not gd.is_finished():
            n += 1
            t += sense()
        t /= n

        # Exit if HOME button pressed
        cc = gd.controllers()
        if cc[0]['bh'] or cc[1]['bh']:
            return

        gd.cmd_gradient(0, 0, 0x000010, gd.w, gd.h, 0x206060)
        gd.VertexFormat(3)
        gd.cmd_text(640, 80, 17, eve.OPT_CENTER, "CPU junction temperature")

        # Draw dot and measurement
        gd.PointSize(20)
        gd.Begin(eve.POINTS)
        y = game.map(t, 0, 40, 650, 160)
        gd.Vertex2f(1000, y)
        gd.cmd_text(1050, int(y), 16, eve.OPT_CENTERY, "%.1f C" % t)
        
        # Update sparkline every 0.1 s
        if (time.time() - t0) > 0.1:
            t0 += 0.1
            sparkline.append((1000, y))
            sparkline = sparkline[-90:]
            sparkline = [(x - 10, y) for (x, y) in sparkline]

        gd.LineWidth(5)
        gd.Begin(eve.LINE_STRIP)
        for (x, y) in sparkline:
            gd.Vertex2f(x, y)
        gd.swap()

if __name__ == "__main__":
    if sys.implementation.name == 'circuitpython':
        gd = eve.Gameduino()
        import microcontroller
        def celsius():
            return microcontroller.cpu.temperature
    else:
        from spidriver import SPIDriver
        gd = eve.GameduinoSPIDriver(SPIDriver(sys.argv[1]))
        def celsius():
            return 24 + time.time() % 2
    temperature(gd, celsius)
