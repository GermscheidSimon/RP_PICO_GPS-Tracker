class Handshake(object):

   

    def __init__(self, dataMsgCount, bodySize, retryThreshold):
        self.curSent = ""
        self.curRXHDR = ""
        self.curRXBDY = ""
        self.curMsgReceived = True
        self.dataMsgCount = dataMsgCount
        self.curDatMsgNbr = 0
        self.bodySize = bodySize
        self.retryThreshold = retryThreshold
        self.handShakeEstablished = False

        self.HandshakeRXMSG = {
        'REQACK': 0, # Client Please Acknowledge
        'AFFSYN': 1, # Affermative sync
        'REQSYN': 2, # Client Sync
        'DATHDR': 3, # Data Header
        'DATMSG': 4,  # DATA MSG
        'ENDMSG': 5,
        'DATTXR': 6,
        'INIT': 7
        }
        self.HanshakeTXMSG = {
            0 : 'AFFSYN', # respond to ACK with affermation msg received
            1 : 'REQSYN', # respond to server Ack with Affermation msg received
            2 : 'DATHDR', # Data header with data details (# of MSGs)
            3 : 'DATACK', # Data header received, proceed with data
            4 : 'MSGREC', # MSG ACK, contains boolean (true if msg received success), current message number
            5 : 'ENDMSG',  # end of communication
            7 : 'REQACK'
        }
        self.Msg = {
            'REQACK': 'REQACKHANSHAKE\n',
            'AFFSYN': 'AFFSYNHANDSHAKE\n',
            'REQSYN': 'REQSYNHANDSHAKE\n',
            'DATHRD': self.buildDataHDR,
            'DATACK': 'DATACKDATATRANSFER\n',
            'ENDMSG': 'ENDMSGENDOFTRANSFER\n',
            'MSGREC': self.buildMSGRX,
            'DATTXR': self.buildDataTXR
        }
        return self

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

    def buildMSGRX(self):
        curMSG = self.curDatMsgNbr

        if self.curMsgReceived:
            return f'MSGRECTRUE{curMSG}\n'
        else: 
            return f'MSGRECFALS{curMSG}\n'

    def readMSGRX(self, curMsg):
        if curMsg[6:9] == 'TRUE':
            self.curMsgReceived = True
        else:
            self.curMsgReceived == False
    
    def buildDataTXR(self, msgBdy):
        datamsg = f"DATTXR{msgBdy}\n"
        return datamsg
    
    def buildDataHDR(self):
        dataHdr = f'DATHDR{self.dataMsgCount}_{self.bodySize}\n'
        return dataHdr
    
    def HandShake_TX(self, retryCount, RX_callBack, dataMsgCallBack):
        currentRX_header = "INIT"
        while not self.handShakeEstablished and self.retryThreshold >= retryCount:
            nextMsgEnum = self.HandshakeRXMSG[currentRX_header]
            
            nextMsgHeader = self.HanshakeTXMSG[nextMsgEnum]
            nextMsg = self.Msg[nextMsgHeader]
            yield nextMsg
            
            if nextMsgEnum == self.HandshakeRXMSG["REQSYN"]:
                self.handShakeEstablished = True
                continue

            msgFromRX = RX_callBack().next()
            if not msgFromRX == None:
                self.RX_nextSent(msgFromRX)
                currentRX_header = self.curRXHDR
            else: 
                retryCount += 1
                if retryCount == 100:
                    raise Exception

        yield self.buildDataHDR()

        while self.dataMsgCount >= self.curDatMsgNbr:
            
            msgFromRX = RX_callBack().next()
            self.readMSGRX(msgFromRX)
            if self.curMsgReceived:
                self.RX_nextSent(msgFromRX)
                currentRX_header = self.curRXHDR
                nextMsgBody = dataMsgCallBack(0).next()
                self.curDatMsgNbr += 1
                yield self.buildDataTXR(nextMsgBody)
            else: 
                 nextMsgBody = dataMsgCallBack(1).next()
                 yield self.buildDataTXR(nextMsgBody)
        
        yield self.Msg['ENDMSG']
        
    def HandShake_RX(self, retryCount, RX_callBack, dataMsgCallBack):
        while not self.handShakeEstablished and self.retryThreshold >= retryCount:
            nextMsg = RX_callBack.next()
            if not nextMsg == None:
                nextMsgEnum = self.HandshakeRXMSG[nextMsg]
                nextMsgHeader = self.HanshakeTXMSG[nextMsgEnum]
                nextMsg = self.Msg[nextMsgHeader]
                yield nextMsg
            else: 
                retryCount += 1
                if retryCount == 100:
                    raise Exception
            

