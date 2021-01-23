import bteve as eve

gd = eve.Gameduino()
gd.init()
import pong
import fruit
import temperature

demos = (pong, fruit, temperature)
sel = 0
prev_touch = False
while True:
    gd.finish()
    c = gd.controllers()[0]
    if not prev_touch:
        if c['bdu']:
            sel = (sel - 1)
        if c['bdd']:
            sel = (sel + 1)
        sel %= len(demos)
    prev_touch = any(c[b] for b in ['bdu', 'bdd'])

    if c['ba']:
        demos[sel].run(gd)

    gd.cmd_romfont(30, 30)
    gd.cmd_romfont(31, 31)
    gd.Clear()

    gd.cmd_text(640,  60, 31, eve.OPT_CENTER, "CircuitPython demos")
    gd.cmd_text(640, 640, 30, eve.OPT_CENTER, "Press A to launch, HOME to return to this menu")
    for i,d in enumerate(demos):
        y = 180 + 120 * i
        if i == sel:
            gd.cmd_fgcolor(0xa06000)
        else:
            gd.cmd_fgcolor(0x003030)
        gd.cmd_button(320, y, 640, 100, 31, eve.OPT_FLAT, d.__name__)

    gd.swap()
    """
    for d in demos:
        print('running demo', d.__name__)
        d.run(gd)
        while True:
            cc = gd.controllers()
            if cc[0]['bh'] == 0 and cc[1]['bh'] == 0:
                break
    """
