Examples


.. code:: python

        
        deck = list(range(1, 53))           # Cards are cells 1-52
        random.shuffle(deck)
        gd.ClearColorRGB(0x00, 0x20, 0x00)
        gd.Clear()
        gd.Begin(eve.BITMAPS)
        for i in range(52):
            x = 3 + (i % 13) * 37           # 13 cards per row
            y = 12 + (i // 13) * 68         # 4 rows
            gd.Cell(deck[i])                # select which card to draw
            gd.Vertex2f(x, y)               # draw the card
        
        
.. image:: /gen/images/0024.png

|

