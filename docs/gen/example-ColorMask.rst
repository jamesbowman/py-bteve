Examples


.. code:: python

        
        gd.PointSize(270)
        gd.Begin(eve.POINTS)
        gd.ColorMask(1, 0, 0, 0)          # red only
        gd.Vertex2f(240 - 100, 136)
        gd.ColorMask(0, 1, 0, 0)          # green only
        gd.Vertex2f(240, 136)
        gd.ColorMask(0, 0, 1, 0)          # blue only
        gd.Vertex2f(240 + 100, 136)
        
        
.. image:: /gen/images/0021.png

|

