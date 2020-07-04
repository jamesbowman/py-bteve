import sys
import os
import importlib

from gameduino_spidriver import GameduinoSPIDriver
import registers as gd3
import common

if __name__ == "__main__":
    # gd = common.LoggingGameduinoSPIDriver()
    gd = GameduinoSPIDriver()
    gd.init()

    sys.path.append("loadable/")
    mod = "dance"
    mod = "grave"
    mod = "cube"
    mod = "celestial"
    mod = "photos"
    rmod = importlib.import_module(mod)

    renderer = rmod.Renderer(gd)

    ti = 0
    while 1:
        try:
            st = os.stat("loadable/" + mod + ".py")
            if (st.st_size > 0) and (st.st_mtime > ti):
                print('reload')
                importlib.reload(rmod)
                ti = st.st_mtime
                renderer = rmod.Renderer(gd)
                renderer.load()
                print('done')
        except FileNotFoundError:
            pass
        renderer.draw()
        gd.swap()
