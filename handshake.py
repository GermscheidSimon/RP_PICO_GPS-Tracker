# pylance aNgRy if this isn't here
from typing import Any, Union


try :
    from machine import Pin, UART
    import utime
except:
    from serial import Serial
    import time

class Handshake(object):
    def __init__(self):
        self.curRXBDY = ""
        self.curRXHDR = ""
        self.data = ""
        self.useMicroPy = True
        self.handShakeEstablished = False
        
        try :
            import machine # WHAT IS MY PURPOSE
        except:
            self.useMicroPy = False
        # Oh . .  My God...
        if self.useMicroPy:
            self.buildMycroPySerial() 
        else:
            self.buildCPySerial()

    def requestLock(self):
        retries = 0
        while not self.handShakeEstablished and retries <= 100:
            self.sleep(2)
            self.writeNextLine('REQACK\n')
            self.sleep(1)
            resMsg = self.readNextLine()
            print(resMsg)
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
        while not self.handShakeEstablished and retries <= 100:
            print(retries)
            self.sleep(2)
            reqMsg = self.readNextLine()
            self.sleep(1)
            print(reqMsg)
            self.RX_nextSent(reqMsg)
            if self.curRXHDR == 'REQACK':
                self.writeNextLine('RESACK\n')
                self.handShakeEstablished = True
                return True
            retries += 1
        return False

    def buildMycroPySerial(self):
        self.serialInt = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13), bits=int(8), parity=None)
        self.readNextLine = self.serialInt.readline
        self.writeNextLine = self.MycroPy_SerialWrite
        self.flush = self.MycroPy_flush
        self.sleep = utime.sleep 
        
    def MycroPy_SerialWrite(self, msg):
        encodedMsg = str(msg).encode('utf-8')
        return self.serialInt.write(encodedMsg) or 0
    
    def buildCPySerial(self): 
        self.serialInt = Serial('/dev/serial0', 9600)
        self.readNextLine = self.serialInt.read_until
        self.writeNextLine =  self.C_PySerialWrite
        self.flush = self.serialInt.flushInput
        self.sleep = time.sleep

    def MycroPy_flush(self):
        self.serialInt.read() #read out buffer
    
    def C_PySerialWrite(self, msg):
        encodedMsg = str(msg).encode('utf-8')
        bits = self.serialInt.write(encodedMsg)
        return bits or 0

    def RX_nextSent(self, nextMsg):
        self.curSent = nextMsg.decode()
        self.curRXHDR = self.curSent[0:6]
        self.curRXBDY = self.curSent[7:-1]


    def TX_data(self, data):
        messages = ['DATSTR', f'DATHDR{data}', 'DATEND']
        self.flush()
        for msg in messages:
            bitSent = self.writeNextLine(msg)
            self.writeNextLine('\n')
            self.sleep(1)
            msgres = self.readNextLine()
            print(msgres)
            self.RX_nextSent(msgres)
            if self.curRXHDR != 'RXTRUE':
                return False
            if  bitSent <= 0:
                return False
        return True
        

    def RX_data(self):
        messages = ['DATSTR', 'DATHDR', 'DATEND']
        data = ""
        self.flush()
        for msg in messages:
            msgres = self.readNextLine()
            print(msgres)
            self.RX_nextSent(msgres)
            if self.curRXHDR == msg:
                self.sleep(1)
                rxtrue = self.writeNextLine('RXTRUE')
                if rxtrue <= 0:
                    return False
            if self.curRXHDR == 'DATHDR':
                self.data = self.curRXBDY
        return True
                


       


