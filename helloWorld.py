from machine import Pin, UART;
import micropyGPS

class piGPS(object):

    def verifyStringID(self):
        nmeaSentence = str(nmeastring)
        nmeaID = nmeaSentence[3:8]
        if nmeaID == "GPRMC":
            return True
        return False

    def readLine(self):
        satSysName = gpsModule.readline()
        return satSysName

    def serialize_GPRMC(self):
        if verifyStringID(nmeaSent):
            for car in str(nmeaSent):
                _gps.update(car)
                return _gps.latitude, _gps.longitude, _gps.timestamp, _gps.date

    def defaultOperation(self):
        index = 0
        while True:
            yield index
            index += 1

    def buildRuntime(self):
        return "ope"

        
    def handleReset(self):
        print("restart placeholder")

    def __init__(self):

        self.lat = 44
        self.long = 93
        self.onBoardLED = Pin(25, Pin.OUT)
        self.gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
        self._gprmcReader = micropyGPS.MicropyGPS()

        try:
            self.buildRuntime()
            self.defaultOperation()
        except:
            self.handleReset()