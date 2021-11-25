
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
        nextState = self.run()
        self.next(nextState)

    def run(self):
        print("Waiting: Broadcasting cheese smell")

    def next(self, curState):
        return self

    # Power full RP on, pass GPS information to RP, and await response
class ConnectingPi(State):
    def __init__(self):
        self.errState = 0
        self.stateName = 'CONNECTPI'

    def run(self):
       try:
           return ('CONNECTPI', self.errState)
       except:
           self.errState = 2
           curState = (self.stateName, self.errState)
           return curState


#==================================================================
# Pico GPS Finite State Machine - Coordination engine for Pico board
#==================================================================
    # Will attempt to independently determine if the GPS coords have changed,
    # and relay that information to the more powerful (and power hungry) RP w/LTE.

class PIGPS(object):
    def __init__(self):
        
        self.curState = (
            'INIT', 0
        )
        self.tasks = [self.curState]

        #after PIGPS determines which is the next action to take, it will call the next transition.
        self.transitions = {
            'READGPS': ReadingGPS,
            'CONNECTPI': ConnectingPi
        }
        self.stateConditions = {
            ('INIT', 0): 'READGPS',
            ('READGPS', 1): 'EVALCOORD',
            ('EVALCOORD', 0): 'READGPS',
            ('EVALCOORD', 1): 'CONNECTPI',
            ('CONNECTPI', 0): 'READGPS'
        }

    def stateDictionary(self, currentState):
        nextTransition = self.stateConditions[currentState]
        return self.transitions[nextTransition]
    
    def runPIGPS(self):
        while len(self.tasks) > 0:
            nextTask = self.stateDictionary(self.tasks[0])

            try:
                nextState = nextTask().run()

                if len(self.tasks) <= 1: # if in error/retry loop don't add more tasks
                    self.tasks.append(nextState)
                self.tasks.pop(0)
                
            except:
                isNotRetry = len(self.tasks) == 1
                if isNotRetry:
                    
                    nextState = (nextTask, 2)
                print('ex not implemented yet', self.curState)
    
    

