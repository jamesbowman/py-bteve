import bteve as eve

gd = eve.Gameduino()
gd.init()
import pong
import fruit
import temperature

demos = (pong, fruit, temperature)
while True:
    for d in demos:
        print('running demo', d)
        d.run(gd)
        while True:
            cc = gd.controllers()
            if cc[0]['bh'] == 0 and cc[1]['bh'] == 0:
                break
