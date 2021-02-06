Examples


.. code:: python

        
        gd.Begin(eve.POINTS)
        gd.PointSize(24);
        for i in range(0, 256, 5):
            gd.ColorA(i)
            gd.Vertex2f(2 * i, 136 + 120 * math.sin(i / 40));
        
        
.. image:: /gen/images/0022.png

|

