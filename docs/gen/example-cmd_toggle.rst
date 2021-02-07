Examples


.. code:: python

        
        gd.cmd_toggle(180,  20, 120, 31, 0, 0,     "yes", "no")
        gd.cmd_toggle(180, 120, 120, 31, 0, 32768, "yes", "no")
        gd.cmd_toggle(180, 220, 120, 31, 0, 65535, "yes", "no")
        
        
.. image:: /gen/images/0027.png

|


.. code:: python

        
        gd.cmd_text(gd.w // 2, 100, 30, eve.OPT_CENTER, "What is your age, Liesl?")
        gd.cmd_toggle(180, 160, 120, 31, eve.OPT_FORMAT, 32768, "%d", "%d", 17, 16)
        
        
.. image:: /gen/images/0028.png

|

