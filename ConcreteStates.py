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
    # TODO: implement proper lat, long, time, date int
    # [self.gpsReader.latitude, self.gpsReader.longitude, self.gpsReader.timestamp, self.gpsReader.date]
    def __init__(self, prevState, origin):
        self.errState = 0
        self.stateName = 'EVALCOORD'
        self.listOfCoords = prevState.data
        self.origin = origin
        self.LongitudinalDistanceFromOrigin = 0
        self.LatitudinalDistanceFromOrigin = 0

    def evaluateMovement(self, listOfCoords, origin):
        AvgLatCoord = 0
        AvgLongCoord = 0
        for coord in listOfCoords:
            AvgLatCoord += GPSCoord().convertDMMToDD(coord.lat)
            AvgLongCoord += GPSCoord().convertDMMToDD(coord.long)
        AvgLongCoord = AvgLongCoord / len(listOfCoords)
        AvgLatCoord = AvgLatCoord / len(listOfCoords)
        self.LatitudinalDistanceFromOrigin = GPSCoord().compareDDCoord(AvgLatCoord, GPSCoord().convertDMMToDD(origin.lat))
        self.LongitudinalDistanceFromOrigin = GPSCoord().compareDDCoord(AvgLongCoord, GPSCoord().convertDMMToDD(origin.long))
        print('lat, long distance from origin: ',self.LatitudinalDistanceFromOrigin, self.LongitudinalDistanceFromOrigin)



    

    def run(self):

        try: 
            movementDetected = self.evaluateMovement(self.listOfCoords, self.origin)
            if movementDetected:
                self.errState = 1
        except:
            self.errState = 2
            raise Exception
