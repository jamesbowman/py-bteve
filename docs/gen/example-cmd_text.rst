Examples


.. code:: python

        
        ipsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris'
        gd.cmd_fillwidth(400)
        gd.ColorRGB(0xf8, 0x80, 0x17) # orange
        gd.cmd_text(40, 10, 30, eve.OPT_FILL, ipsum)
        
        
.. image:: /gen/images/0029.png

|


.. code:: python

        
        gd.ColorRGB(0x00, 0x00, 0x00)
        gd.Begin(eve.LINES)
        gd.Vertex2f(240, 0)
        gd.Vertex2f(240, gd.h)
        gd.ColorRGB(0xff, 0xff, 0xff)
        gd.cmd_text(240, 50, 29, 0, "default")
        gd.cmd_text(240,100, 29, eve.OPT_RIGHTX, "eve.OPT_RIGHTX")
        gd.cmd_text(240,150, 29, eve.OPT_CENTERX, "eve.OPT_CENTERX")
        
        
.. image:: /gen/images/0030.png

|


.. code:: python

        
        t = 31.09
        gd.cmd_text(240,100, 29, eve.OPT_FORMAT | eve.OPT_CENTER,
                    "Temperature is %d.%02d C", int(t), int(t * 100) % 100)
        
        
.. image:: /gen/images/0031.png

|

