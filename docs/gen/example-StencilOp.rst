Examples


.. code:: python

        
        gd.StencilOp(eve.INCR, eve.INCR); # incrementing stencil
        gd.PointSize(270)
        gd.Begin(eve.POINTS)              # Draw three white circles
        gd.Vertex2ii(240 - 100, 136)
        gd.Vertex2ii(240, 136)
        gd.Vertex2ii(240 + 100, 136)
        gd.ColorRGB(0xff, 0x00, 0x00)     # Draw pixels with stencil==2 red
        gd.StencilFunc(eve.EQUAL, 2, 255)
        gd.Begin(eve.RECTS);              # Paint every pixel on the screen
        gd.Vertex2f(0,0); gd.Vertex2f(480,272)
        
        
.. image:: /gen/images/0019.png

|

