import Handshake
import json
import utime

class ConnectPi(object):

    def __init__(self):
        return self

    def transferCoord(self, coord):
        handshake = Handshake.Handshake()
        #encode obj to json
        jsonObj = json.dumps({"lat": f'{coord.lat}', "long": f'{coord.long}', "date": f'{coord.date}', "time": f'{coord.time}'})

        handshakeLock = handshake.requestLock()
        if handshakeLock:
            isSent = handshake.TX_data(jsonObj)
            if isSent:
                return True
            else:
                return False
    def raceCodnitionLoL(self):
        utime.sleep(2)
        print('RP TURNED ON')
        utime.sleep(5)

