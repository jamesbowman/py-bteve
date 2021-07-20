import os
import sys
import time
import bteve as eve

gd = eve.Gameduino()
gd.init()

print(os.listdir("/sd"))
FN = "/sd/spa-1500.avi"
L = 825478
t0 = time.monotonic()
if 0:
    gd.cmd_memwrite(0, L)
    with open(FN, "rb") as f:
        gd.load(f)
    gd.finish()
else:
    with open(FN, "rb") as f:
        a = 0
        while True:
            s = f.read(2048)
            if not s:
                break
            gd.wr(a, s)
            a += len(s)
        assert a == L
t1 = time.monotonic()
took = t1 - t0
rate = (L / took) / 1024
print(f"took {took:.3f} s, {rate:.3f} Kbytes/s")

"""

512 byte chunks
Pico:    took 4.022 s, 200.430 Kbytes/s
Metro:   took 2.869 s, 280.980 Kbytes/s
Teensy:  took 1.951 s, 413.188 Kbytes/s
Feather: took 2.799 s, 288.024 Kbytes/s

Pico:    took 3.727 s, 216.294 Kbytes/s
Metro:   took 2.773 s, 290.707 Kbytes/s
Teensy:  took 1.514 s, 532.395 Kbytes/s
Feather: took 2.677 s, 301.132 Kbytes/s

"""
