from PIL import Image
import numpy as np
import math

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

    return Image.fromarray((255 * np.clip(lum, 0, 1).reshape((h, w))).astype(np.uint8), "L")

if __name__ == '__main__':
    im = light(23, 134)
    im.save("out.png")
