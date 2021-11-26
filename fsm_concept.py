
from ConcreteStates import *;

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

        # After PIGPS determines which is the next action to take, it will call the next transition.
        self.transitions = {
            'READGPS': ReadingGPS,
            'CONNECTPI': ConnectingPi,
            'EVALCOORD': EvalCoord
        }
        self.stateConditions = {
            ## == Error Code Definitions == ##
                #  0 -- Default Path (happy path)
                #  1 -- Movement Detected 
                #  2 -- Exception State 
            ('INIT', 0): 'READGPS',       # (Initial State, Default path) proceed to READGPS
            ('READGPS', 0): 'EVALCOORD',  # (GPS state read, Default path) proceed to evaluate GPS coords
            ('EVALCOORD', 0): 'READGPS',  # (GPS evaluated, Default path) no movement detected, proceed back to GPS read
            ('EVALCOORD', 1): 'CONNECTPI',# (GPS evaluated, movement Detected) power on RP and pass priority to RP
            ('CONNECTPI', 0): 'READGPS'   # (PI connected, return to default path) read current GPS

        }

    def stateDictionary(self, currentState):
        print('current state', currentState)
        nextTransition = (self.stateConditions[currentState])
        print('next transition found: ', nextTransition)
        nextState = self.transitions[nextTransition]
        return nextState
    
    def runPIGPS(self):
        while len(self.tasks) > 0:
            print('runGPS loop. Task:', self.tasks)
            nextTask = self.stateDictionary(self.tasks[0])

            try:
                State = nextTask()
                State.run()

                if len(self.tasks) <= 1: # if in error/retry loop don't add more tasks
                    self.tasks.append((State.stateName, State.errState))
                self.tasks.pop(0)
                
            except:
                print('in exception loop', self.curState)
                isNotRetry = len(self.tasks) == 1
                if isNotRetry:
                    nextState = (nextTask, 2)
    
    

