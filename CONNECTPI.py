from machine import Pin, UART


rpzero = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), bits=int(8), parity=None)
testing = 'TESTaa'
rpzero.write("A123")
utime.sleep(1)
print(rpzero.read(10), count)
count += 1


class Handshake(object):

    def __init__(self, RX_Pin, TX_Pin, baud):

        self.RX_Pin = Pin(RX_Pin)
        self.TX_Pin = Pin(TX_Pin)
        self.baud = baud
        self.uart = UART(1, baudrate=self.baud, tx=self.TX_Pin, rx=self.RX_Pin, bits=int(8), parity=None)
        self.curMsg = ""
        return self