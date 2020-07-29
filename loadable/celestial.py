# https://visibleearth.nasa.gov/collection/1484/blue-marble?page=2
# https://www.celestrak.com/NORAD/elements/

# Three layers (day, night, clouds)
# 2**23 / (1280*640) / 3 = 3.41  ==> ASTC_8x5
# 160x128x16 = 327680
# leaves 64K for other things
# day/night matte: L8 256x128

import datetime
from datetime import timezone
import time
import math
import struct
import numpy as np

import ephem

from PIL import Image
from gameduino_spidriver import GameduinoSPIDriver
import registers as gd3
import common
from common import Pt

def subsolar_point(t):
    greenwich = ephem.Observer()
    greenwich.lat = "0"
    greenwich.lon = "0"
    greenwich.date = datetime.datetime.fromtimestamp(t, timezone.utc)
    sun = ephem.Sun(greenwich)
    sun.compute(greenwich.date)
    sun_lon = math.degrees(sun.ra - greenwich.sidereal_time() )
    if sun_lon < -180.0 :
      sun_lon = 360.0 + sun_lon 
    elif sun_lon > 180.0 :
      sun_lon = sun_lon - 360.0
    sun_lat = math.degrees(sun.dec)
    return (sun_lat, sun_lon)

def rad(deg):
    return deg * math.pi / 180

def light(sun_lat, sun_lon):
    (w, h) = (256, 128)
    a = np.tile(np.linspace(-180, 180, w), h)
    d = np.repeat(np.linspace(90, -90, h), w)

    def xyz(a, d):
        x = np.cos(rad(d)) * np.cos(rad(a))
        y = np.cos(rad(d)) * np.sin(rad(a))
        z = np.sin(rad(d))
        return (x, y, z)

    earth = xyz(a, d)
    solar = xyz(sun_lon, sun_lat)
    lum = sum([a * b for (a, b) in zip(earth, solar)])
    lum = np.power(np.maximum(0, lum), 0.7)

    return Image.fromarray((255 * np.clip(lum, 0, 1).reshape((h, w))).astype(np.uint8), "L")

class Renderer:
    
    def __init__(self, gd):
        self.gd = gd
        self.t = 0

    version = 102

    def load(self):
        gd = self.gd

        Mloc = 0
        if gd.rd32(Mloc) != self.version:
            ld = common.Loader(gd)
            ld.add(struct.pack("4I", self.version, 0, 0, 0))
            gd.BitmapHandle(0)
            ld.Lastc("assets/celestial-day.astc")
            gd.BitmapHandle(1)
            ld.Lastc("assets/celestial-night.astc")
        print(hex(gd.rd32(Mloc)))

    def draw(self):
        gd = self.gd

        y0 = 720 - 640

        t = time.time() # + 180 * 24 * 3600
        t = time.time() + self.t * 600
        (sun_lat, sun_lon) = subsolar_point(t)
        print(self.t, sun_lat, sun_lon)
        x = 640 + 640 * sun_lon / 180
        y = y0 + 320 - 320 * sun_lat / 90

        lim = light(sun_lat, sun_lon)
        ld = common.Loader(gd)
        ld.a = (1 << 20) - (256 * 128)
        gd.BitmapHandle(2)
        ld.L8(lim)
        gd.BitmapSize(gd3.BILINEAR, gd3.REPEAT, gd3.BORDER, 0, 0)

        gd.VertexFormat(2)

        # Match the color of the arctic
        br = lim.load()[128, 0] / 255
        r = int(common.lerp(br, 27, 255))
        g = int(common.lerp(br, 27, 255))
        b = int(common.lerp(br, 55, 255))
        gd.ClearColorRGB(r, g, b)
        gd.Clear()
        gd.Begin(gd3.BITMAPS)
        gd.SaveContext()
        gd.BitmapHandle(1)
        i = 180
        gd.ColorRGB(i, i, i)
        gd.Vertex2f(0, y0)
        gd.RestoreContext()

        gd.SaveContext()
        sf = 1280 / 256
        gd.cmd_scale(sf, sf)
        gd.cmd_setmatrix()
        gd.BitmapHandle(2)
        gd.ColorMask(0, 0, 0, 1)
        gd.BlendFunc(1, 0)
        gd.Vertex2f(0, y0)
        gd.RestoreContext()

        gd.SaveContext()
        gd.BlendFunc(gd3.DST_ALPHA, gd3.ONE_MINUS_DST_ALPHA)
        gd.BitmapHandle(0)
        gd.Vertex2f(0, y0)
        gd.RestoreContext()

        gd.SaveContext()
        gd.Begin(gd3.POINTS)
        gd.ColorRGB(80, 70, 30)
        gd.BlendFunc(gd3.SRC_ALPHA, gd3.ONE)
        for i in range(50, 250, 50):
            gd.PointSize(i)
            gd.Vertex2f(x, y)
        gd.RestoreContext()

        dt = datetime.datetime.fromtimestamp(t, timezone.utc)
        if 0:
            gd.SaveContext()
            gd.ColorRGB(0, 0, 0)
            gd.cmd_text(640, 3, 31, gd3.OPT_CENTERX,
                dt.ctime())
            gd.RestoreContext()

        if 0:
            for i in range(25):
                hr = (dt.hour - 12 + i) % 12
                gd.cmd_clock(1280 * i // 24, 30, 20, gd3.OPT_FLAT | gd3.OPT_NOSECS,
                             hr, dt.minute, 0, 0)

        self.t += 1
        # gd.screenshot_im().save("out.png"); sys.exit(0);
        # time.sleep(10)
        assert self.t < 180
