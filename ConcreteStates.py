import gps_module;


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
        

    def next(self, curState):
        return self

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
    def __init__(self, prevState, origin):
        self.errState = 0
        self.stateName = 'EVALCOORD'
        self.listOfCoords = prevState.data
        self.origin = origin

    def evaluateMovement(self, listOfCoords, origin):
        for coord in listOfCoords:
            if coord < origin + 10 and coord > origin -10:
                print('eval res- no movement detected')
                return False
            else:
                print('eval res- movement detected')
                return True

    def run(self):

        try: 
            movementDetected = self.evaluateMovement(self.listOfCoords, self.origin)
            if movementDetected:
                self.errState = 1
        except:
            self.errState = 2
            raise Exception

