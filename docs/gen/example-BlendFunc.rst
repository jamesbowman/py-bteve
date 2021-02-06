Examples


.. code:: python

        
        gd.Begin(eve.POINTS)
        gd.ColorRGB(0xf8, 0x80, 0x17)
        gd.PointSize(160)
        gd.BlendFunc(eve.SRC_ALPHA, eve.ONE_MINUS_SRC_ALPHA)
        gd.Vertex2f(150, 76); gd.Vertex2f(150, 196)
        gd.BlendFunc(eve.SRC_ALPHA, eve.ONE)
        gd.Vertex2f(330, 76); gd.Vertex2f(330, 196)
        
        
.. image:: /gen/images/0024.png

|

