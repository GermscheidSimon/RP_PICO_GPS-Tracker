from machine import Pin, UART;
import utime;
import micropyGPS;


onBoardLED = Pin(25, Pin.OUT)
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
print(gps_module)

_gps = micropyGPS.MicropyGPS()


def verifyStringID(nmeastring):
    nmeaSentence = str(nmeastring)
    nmeaID = nmeaSentence[3:8]
    if nmeaID == "GPRMC":
        return True
    return False

def readLine(gpsModule):
    satSysName = gpsModule.readline()
    return satSysName

def serialize_GPRMC(nmeaSent):
    if verifyStringID(nmeaSent):
        for car in str(nmeaSent):
            _gps.update(car)
            return _gps.latitude, _gps.longitude, _gps.timestamp, _gps.date

def defaultOperation():
    index = 0
    while True:
        yield index
        index += 1

def buildRuntime():
    return

    
def handleReset():
    print("restart placeholder")

def __init__():
    try:
        buildRuntime()
        defaultOperation()
    except:
        handleReset()