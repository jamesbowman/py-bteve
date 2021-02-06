Examples


.. code:: python

        
        gd.Begin(eve.POINTS)
        for x in range(0, 480, 40):
            gd.PointSize(x / 10)
            gd.ColorRGB(0xff, random.randrange(256), random.randrange(256))
            gd.Vertex2f(x, random.randrange(272))
        
        
.. image:: /gen/images/0017.png

|

