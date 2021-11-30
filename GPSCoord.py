from typing import Tuple


class GPSCoord(object):

    def __init__ (self):
        self.lat = [0, 0.0, 'N']
        self.long = [0, 0.0, 'W']
        self.date = []
        self.time = []

    def compareDMMCoord(self, firstCoord, SecondCoord):
        firstCoord_DD = self.convertDMMToDD(firstCoord)
        SecondCoord_DD = self.convertDMMToDD(SecondCoord)
        distance = int(0)
        if firstCoord_DD >= SecondCoord_DD:
            distance = firstCoord_DD - SecondCoord_DD
        else:
            distance = SecondCoord_DD - firstCoord_DD
        if distance < 0:
            distance * -1
        return distance

    def compareDDCoord(self, firstCoord, SecondCoord):
        distance = 0
        if firstCoord >= SecondCoord:
            distance = firstCoord - SecondCoord
        else:
            distance = SecondCoord - firstCoord
        if distance < 0:
            distance * -1
        return distance



    def convertDMMToDD(self, coord):
        # one degree = 60 minutes
        # one minutes = 60 seconds
        # micropyGPS returns DD, MM.MM format
        degrees = coord[0] 
        minutes = coord[1] / 60
        ddFormat = int(degrees + minutes)

        #flip to negative if S or E coord
        if coord[2] == "S" or coord[2] == "E":
            ddFormat * -1 

        return ddFormat
        
        
        

