import handshake
import json
import utime

class ConnectPi(object):

    def __init__(self):
        self.transferSuccess = False

    def transferCoord(self, coord):
        handshake = handshake.Handshake()
        #encode obj to json
        jsonObj = json.dumps({"lat": f'{coord.lat}', "long": f'{coord.long}', "date": f'{coord.date}', "time": f'{coord.time}'})
        self.raceCodnitionLoL()
        handshakeLock = handshake.requestLock()
        if handshakeLock:
            isSent = handshake.TX_data(jsonObj)
            if isSent:
                self.transferSuccess = True
                return self.transferSuccess
            else:
                self.transferSuccess = False
                return self.transferSuccess

    def raceCodnitionLoL(self):
        utime.sleep(2)
        print('RP TURNED ON')
        utime.sleep(5)

