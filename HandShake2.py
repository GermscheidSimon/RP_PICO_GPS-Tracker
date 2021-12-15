try :
    from machine import Pin, UART
    import utime
except:
    from serial import Serial
    import time

class Handshake(object):
    def __init__(self):
        self.useMicroPy = True
        self.handShakeEstablished = False
        
        try :
            import machine
        except:
            self.useMicroPy = False
        
        if self.useMicroPy:
            self.buildMycroPySerial()
        else:
            self.buildCPySerial()

    def requestLock(self):
        retries = 0
        while not self.handShakeEstablished and retries <= 100:
            self.sleep(2)
            self.writeNextLine('REQACK')
            self.sleep(1)
            resMsg = self.readNextLine()
            if not resMsg == None:
                self.RX_nextSent(resMsg)
                if self.curRXHDR == 'RESACK':
                    self.handShakeEstablished = True
                    return True
            print(retries) 
            retries += 1
        return False
    
    def respondLock(self):
        retries = 0
        while self.handShakeEstablished and retries <= 100:
            self.sleep(2)
            reqMsg = self.readNextLine()
            self.sleep(1)
            self.RX_nextSent(reqMsg)
            if self.curRXHDR == 'REQACK':
                self.writeNextLine('RESACK')
                self.handShakeEstablished = True
                return True
            retries += 1
        return False

    def buildMycroPySerial(self):
        self.serialInt = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), bits=int(8), parity=None)
        self.readNextLine = self.serialInt.readline
        self.writeNextLine = self.MycroPy_SerialWrite
        self.sleep = utime.sleep
        
    def MycroPy_SerialWrite(self, msg):
        encodedMsg = str(msg).encode('utf-8')
        self.serialInt.write(encodedMsg)
    
    def buildCPySerial(self):
        self.serialInt = Serial('/dev/serial0', 9600)
        self.readNextLine = self.serialInt.read_until
        self.writeNextLine = self.C_PySerialWrite
        self.sleep = time.sleep

    def C_PySerialWrite(self, msg):
        encodedMsg = str(msg).encode('utf-8')
        self.serialInt.write(encodedMsg)

    def RX_nextSent(self, nextMsg):
        self.curSent = nextMsg
        startofLine = nextMsg[0] == 'b'
        if startofLine:
            trimmedMsg = nextMsg[2, nextMsg[-1]] # msg [b,',m,s,g,s,t,r,i,n,g,']
            self.curRXHDR = trimmedMsg[0, 5]
            self.curRXBDY = trimmedMsg[6, trimmedMsg[-1]]
            return True
        else:
            return False