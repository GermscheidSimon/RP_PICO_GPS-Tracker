#======================================================
# Concrete States                                     #
#======================================================

    # Base class for all concrete states
class State(object):
    # each state will use the constructor to run the concrete operation
    # next will then pass the result of run to the state machine to call next operation
    def __init__(self):
        nextState = self.run()
        self.next(nextState)

    def run(self):
        print("execute concrete state operation")

    def next(self, input):
        print("determine next move")
        return "next move is..."

    # Connect to GPS Module, gather 10 gps coordinates, export to piGPS to transition
class ReadingGPS(State):
    def __init__(self):
        self.errState = 0
        self.stateName = 'READGPS'
        self.data = []

    def run(self):
        print('it runned')
        

    def next(self, curState):
        return self

    # Power full RP on, pass GPS information to RP, and await response
class ConnectingPi(State):
    def __init__(self):
        self.errState = 0
        self.stateName = 'CONNECTPI'

    def run(self):
       try:
           print('connecting To Pi')
       except:
           self.errState = 2
           curState = (self.stateName, self.errState)
           return curState

class EvalCoord(State):
    # TODO: implement proper lat, long, time, date int
    def __init__(self):
        self.errState = 0
        self.stateName = 'EVALCOORDS'

    def evaluateMovement(self, listOfCoords, origin):
        for coord in listOfCoords:
            if coord > origin + 10 or coord < origin -10:
                print('eval res- no movement detected')
                return False
            else:
                print('eval res- movement detected')
                return True

    def run(self, listOfCoords, origin):

        try: 
            movementDetected = self.evaluateMovement(listOfCoords, origin)
            if movementDetected:
                self.errState = 1
        except:
            self.errState = 2
            raise Exception

