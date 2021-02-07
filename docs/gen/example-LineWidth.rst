Examples


.. code:: python

        
        gd.Begin(eve.LINE_STRIP)
        for x in range(0, 480, 40):
            gd.LineWidth(x / 10)
            gd.ColorRGB(0xff, random.randrange(256), random.randrange(256))
            gd.Vertex2f(x, random.randrange(272))
        
        
.. image:: /gen/images/0014.png

|

