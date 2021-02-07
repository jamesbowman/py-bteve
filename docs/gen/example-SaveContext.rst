Examples


.. code:: python

        
        gd.cmd_text(240,  64, 31, eve.OPT_CENTER, "WHITE")
        gd.SaveContext()
        gd.ColorRGB(0xff, 0x00, 0x00)
        gd.cmd_text(240, 128, 31, eve.OPT_CENTER, "RED")
        gd.RestoreContext()
        gd.cmd_text(240, 196, 31, eve.OPT_CENTER, "WHITE AGAIN")
        
        
.. image:: /gen/images/0017.png

|

