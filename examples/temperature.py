import sys
import time
import bteve as eve

import game

def temperature(gd, sense):
    gd.cmd_romfont(16, 33)
    gd.cmd_romfont(17, 34)

    sparkline = []
    t0 = time.monotonic()
    temp = sense()
    frames = 0
    while True:
        # Measure temp continuously until CPU is ready to redraw
        # then compute average

        gd.flush()
        while not gd.is_finished():
            temp = (999 * temp + sense()) / 1000

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
        y = game.map(temp, 0, 50, 650, 160)
        gd.Vertex2f(1000, y)
        gd.cmd_text(1050, int(y), 16, eve.OPT_CENTERY, "%.1f C" % temp)
        
        # Update sparkline every 0.1 s
        frames += 1
        if (frames % 6) == 0:
            sparkline.append((1000, y))
            sparkline = sparkline[-90:]
            sparkline = [(x - 10, y) for (x, y) in sparkline]

        gd.LineWidth(5)
        gd.Begin(eve.LINE_STRIP)
        for (x, y) in sparkline:
            gd.Vertex2f(x, y)
        gd.swap()

if sys.implementation.name == 'circuitpython':
    import microcontroller
    def celsius():
        return microcontroller.cpu.temperature
    def run(gd):
        temperature(gd, celsius)
elif __name__ == "__main__":
    from spidriver import SPIDriver
    gd = eve.GameduinoSPIDriver(SPIDriver(sys.argv[1]))
    def celsius():
        return 24 + time.monotonic() % 2
    temperature(gd, celsius)
