import Handshake

class rpConnectZero(object):
    def __init__(self):
        self.handshake = Handshake.Handshake() # expose handshake so data can be recovered

    def RX_data(self):
       
        handshakeLock = self.handshake.respondLock()
        if handshakeLock:
            isSent = self.handshake.RX_data()
            if isSent:
                return True
            else:
                return False
        self.printData()

    def printData(self):
        print(self.handshake.data)