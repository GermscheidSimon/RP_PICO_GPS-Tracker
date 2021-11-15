from machine import Pin, UART;
import utime;
import micropyGPS;


onBoardLED = Pin(25, Pin.OUT)
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
print(gps_module)

_gps = micropyGPS.MicropyGPS()


def verifyStringID(string):
    nmeaSentence = str(string)
    nmeaID = nmeaSentence[3:8]
    if nmeaID == "GPRMC":
        return True
    return False



def run():
    while True:
        utime.sleep(.1)
        satSysName = gps_module.readline()
        if verifyStringID(satSysName):
            for car in str(satSysName):
                _gps.update(car)
            print(_gps.latitude, _gps.longitude, _gps.timestamp, _gps.date)

def infinite():
    index = 0
    while True:
        yield index
        index += 1
    
test = infinite()

while True:
    print(next(test))