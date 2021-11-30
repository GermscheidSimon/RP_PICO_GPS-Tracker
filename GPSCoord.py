from math import radians, cos, sin, asin, sqrt


class GPSCoord(object):

    def __init__ (self):
        self.lat = [0, 0.0, 'N']
        self.long = [0, 0.0, 'W']
        self.date = []
        self.time = []

    # haversine implementation to calculate rough distance between two points on a sphere (closer to the poles the less accurate this can be)
    # (the earth is not a perfect sphere)
    def haversine(self, lat1, lon1, lat2, lon2):

        R = 3959.87433 # this is in miles.  For Earth radius in kilometers use 6372.8 km

        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a))
        return R * c
   
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
        
        
        

