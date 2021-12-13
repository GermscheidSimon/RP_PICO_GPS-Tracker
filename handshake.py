class Handshake(object):

   

    def __init__(self, dataMsgCount, bodySize):
        self.curSent = ""
        self.curRXHDR = ""
        self.curRXBDY = ""
        self.curMsgReceived = True
        self.dataMsgCount = dataMsgCount
        self.curDatMsgNbr = 0
        self.bodySize = bodySize
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
    
    def buildDataTXR(self, msgBdy):
        datamsg = f"DATTXR{msgBdy}\n"
        return datamsg
    
    def buildDataHDR(self):
        dataHdr = f'DATHDR{self.dataMsgCount}_{self.bodySize}\n'
        return dataHdr
    
    def HandShake_TX(self):
        currentTx_header = "INIT"

        if not self.handShakeEstablished:
            nextMsgEnum = self.HandshakeRXMSG[currentTx_header]
            nextMsgHeader = self.HanshakeTXMSG[nextMsgEnum]
            nextMsg = self.Msg[nextMsgHeader]
            yield nextMsg
            
        if self.handShakeEstablished:


