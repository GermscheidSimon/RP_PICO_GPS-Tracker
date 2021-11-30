from machine import Pin, UART;
import utime;
import micropyGPS
from GPSCoord import GPSCoord;

        # lat = [0, 0.0, "N"]
        # long = [0, 0.0, "w"]
class piGPS(object):

    def verifyStringID(self, nmeaSent):
        nmeaString = str(nmeaSent)
        nmeaID = nmeaString[3:8]
        if nmeaID == "GPRMC":
            return True
        return False

    def CheckIfValidCoord(self, coordArray):
        isValidCoord = False
        degree = coordArray[0] != 0
        minute = coordArray[1] != 0.0
        if degree and minute:
            isValidCoord = True
        return isValidCoord
    
    # open connection and read in the next line and check if it has gps data
    # this is to verify if the u-blox gps module has a lock yet and is returning good data. 
    # if no data found, wait 5 seconds.
    # retry up to 20 times
    def attemptLock(self):
        retryCount = 20
        self.gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
        print(self.gps_module)
        while retryCount > 0:
            utime.sleep(.1)
            nmeaSent = self.gps_module.readline()
            utime.sleep(.1)

            print('al', nmeaSent)
            if self.verifyStringID(nmeaSent):
                newCoord = self.serializeNMEAtoCoord(nmeaSent)
                lat = newCoord.lat
                long = newCoord.long
                if self.CheckIfValidCoord(lat) and self.CheckIfValidCoord(long):
                    print('gps module Lock found')
                    return True
                else:
                    print('no lock, retries left:', retryCount)
                    retryCount -= 1
                    utime.sleep(5)
        print ('lock failed')
        return False


        
    def __init__(self):
        self.lat = 44
        self.long = 93
        self.onBoardLED = Pin(25, Pin.OUT)
        self.gpsReader = micropyGPS.MicropyGPS()
        self.data = []
        self.moduleGPSlock = self.attemptLock() # note- time consuming I/O blocking processs!!
        if not self.moduleGPSlock: # if no lock established in 100seconds break out of read process
            raise Exception 

    def serializeNMEAtoCoord(self, nmeaSent):
        for char in str(nmeaSent):
            self.gpsReader.update(char)
        coord = GPSCoord()
        coord.lat = self.gpsReader.latitude
        coord.long = self.gpsReader.longitude
        coord.time = [self.gpsReader.timestamp]
        coord.date = [self.gpsReader.date]
        return coord

    def run(self):
        try:
            nmeaSentCount = 0
            badReadCount = 0
            while nmeaSentCount <= 10:
                
                utime.sleep(.1) #questionable 'await'
                nextSent = self.gps_module.readline()
                utime.sleep(.1) #questionable 'await'
                print(nextSent)

                if self.verifyStringID(nextSent):
                    nextCoord = self.serializeNMEAtoCoord(nextSent)
                    if self.CheckIfValidCoord(nextCoord):
                        self.data.append(nextCoord)
                        nmeaSentCount += 1
                        print(nextCoord)
                    else:
                        badReadCount += 1

                if badReadCount > 20:
                    establishednewLock = self.attemptLock()
                    if not establishednewLock:
                        raise Exception
        except:
            raise Exception