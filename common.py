from gameduino_spidriver import GameduinoSPIDriver

class LoggingGameduinoSPIDriver(GameduinoSPIDriver):
    
    def __init__(self):
        GameduinoSPIDriver.__init__(self)

        self.seq = 0
        self.spool()

    def spool(self):
        self.cmd_dump = open("%04d.cmd" % self.seq, "wb")
        self.seq += 1

    def write(self, s):
        GameduinoSPIDriver.write(self, s)
        self.cmd_dump.write(s)

    def swap(self):
        GameduinoSPIDriver.swap(self)
        self.spool()


