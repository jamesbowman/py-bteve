from skyfield.api import Topos, load

ts = load.timescale(builtin=True)
t = ts.now()

planets = load('de421.bsp')
mars = planets['mars']

# From the center of the Solar System (Barycentric)

barycentric = mars.at(t)

# From the center of the Sun (Heliocentric)

sun = planets['sun']
heliocentric = sun.at(t).observe(mars)

# From the center of the Earth (Geocentric)

earth = planets['earth']
astrometric = earth.at(t).observe(sun)
# print(astrometric.subpoint())
