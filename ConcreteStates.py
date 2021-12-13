import gps_module;
from GPSCoord import GPSCoord;

#======================================================
# Concrete States                                     #
#======================================================
  # Concrete States represent static procedures for the machine to perform
  # any given set of tasks

    # ================================ #
    # Base class for all concrete states
class State(object):
    # each state will use the constructor to run the concrete operation
    # next will then pass the result of run to the state machine to call next operation
    def __init__(self, prevState, origin):
        self.errState = 0
        self.stateName = 'BASECLASS'
        self.data = []

    def run(self):
        print("execute concrete state operation")

    def next(self, input):
        print("determine next move")
        return "next move is..."

    # Connect to GPS Module, gather 10 gps coordinates, export to piGPS to transition
class ReadingGPS(State):
    def __init__(self, prevState, origin):
        self.errState = 0
        self.stateName = 'READGPS'
        self.data = []
        self.prevState = prevState
        self.origin = origin

    def run(self):
        try:
            _gpsModule = gps_module.piGPS()
            _gpsModule.run()
            self.data = _gpsModule.data
        except:
            self.errState = 2
            raise Exception

    # Power full RP on, pass GPS information to RP, and await response
class ConnectingPi(State):
    def __init__(self, prevState, origin):
        self.errState = 0
        self.stateName = 'CONNECTPI'
        self.prevState = prevState
        self.origin = origin


    def run(self):
       try:
           print('connecting To Pi')
       except:
           self.errState = 2
           curState = (self.stateName, self.errState)
           return curState

class EvalCoord(State):
    def __init__(self, prevState, origin):
        self.errState = 0
        self.stateName = 'EVALCOORD'
        self.listOfCoords = prevState.data
        self.origin = origin
        self.distanceFromOriginInmi = 0
        self.movementDetectedThreshold = 0.0568182 # ~250 ft in mi

    def evaluateMovement(self, listOfCoords, origin):
        AvgLatCoord = 0
        AvgLongCoord = 0
        AvgLatDegrees = 0
        AvgLatMins = 0
        AvgLongDegrees = 0
        AvgLongMins = 0
        # build average coord from data provided
        for coord in listOfCoords:
            AvgLatDegrees += coord.lat[0]
            AvgLatMins += coord.lat[1]
            AvgLongDegrees += coord.long[0]
            AvgLongMins += coord.long[1]
        
        AvgLatDegrees = AvgLatDegrees / len(listOfCoords)
        AvgLatMins = AvgLatMins / len(listOfCoords)
        AvgLongDegrees = AvgLongDegrees / len(listOfCoords)
        AvgLongMins = AvgLongMins / len(listOfCoords)

        # convert to DD for haversin simplicity
        AvgLongCoord = [AvgLatDegrees, AvgLatMins, listOfCoords[0].lat[2]]
        AvgLatCoord = [AvgLongDegrees, AvgLongMins, listOfCoords[0].long[2]]

        # convert origin to Decimal Degrees
        originlatDD = GPSCoord().convertDMMToDD(origin.lat)
        originlongDD = GPSCoord().convertDMMToDD(origin.long)
        self.distanceFromOriginInmi = GPSCoord().haversine(GPSCoord().convertDMMToDD(AvgLatCoord), GPSCoord().convertDMMToDD(AvgLongCoord), originlatDD, originlongDD)  
        print('distance from origin:', self.distanceFromOriginInmi)
        if self.distanceFromOriginInmi >= self.movementDetectedThreshold:
            newOriginCoord = GPSCoord()
            newOriginCoord.lat = AvgLatCoord
            newOriginCoord.long = AvgLongCoord
            newOriginCoord.date = listOfCoords[0].date
            newOriginCoord.time = listOfCoords[0].time
            self.errState = 1
            self.origin = newOriginCoord
    
    def run(self):

        try:
            self.evaluateMovement(self.listOfCoords, self.origin)
            print('update origin: ', self.origin.lat, self.origin.long)

        except:
            self.errState = 2
            raise Exception


class exept(State):
    # I assume something bad happened if you're reading this
    def __init__(self, prevState, origin):
        self.prevState = prevState
        self.origin = origin
        return self

    def run(self):
        return self
