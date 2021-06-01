import sys
import time
import bteve as eve

if __name__ == "__main__":
    if sys.implementation.name == "circuitpython":
        gd = eve.Gameduino()
        D = "/sd/"
    else:
        from spidriver import SPIDriver
        gd = eve.Gameduino(SPIDriver(sys.argv[1]))
        D = "sd/"
    gd.init()

    while 1:
        for fn in ("fun-1500.avi", "tra-1500.avi", "fish.avi"):
            with open(D + fn, "rb") as f:
                mp = eve.MoviePlayer(gd, f)
                mp.play()
