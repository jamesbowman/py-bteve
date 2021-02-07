Examples


.. code:: python

        
        def zigzag(title, x):
            for i in range(3):
              gd.Vertex2f(x - 14,   25 + i * 90)
              gd.Vertex2f(x + 14,   25 + 45 + i * 90)
            gd.cmd_text(x, 0, 27, eve.OPT_CENTERX, title)
        
        gd.Begin(eve.BITMAPS)
        zigzag("BITMAPS", 48)
        
        gd.Begin(eve.POINTS)
        zigzag("POINTS",  48 + 1 * 96)
        
        gd.Begin(eve.LINES)
        zigzag("LINES",  48 + 2 * 96)
        
        gd.Begin(eve.LINE_STRIP)
        zigzag("LINE_STRIP",  48 + 3 * 96)
        
        gd.Begin(eve.RECTS)
        zigzag("RECTS",  48 + 4 * 96)
        
        
.. image:: /gen/images/0025.png

|

