from ConcreteStates import *;

#==================================================================
# Pico GPS Finite State Machine - Coordination engine for Pico board
#==================================================================
    # Will attempt to independently determine if the GPS coords have changed,
    # and relay that information to the more powerful (and power hungry) RP w/LTE.

# TODO:
    # create Location class to better model coordinates and origin info
    # verify retry capability with current exception system

class PIGPS(object):
    def __init__(self):
        
        self.curTask = (
            'INIT', 0
        )
        self.tasks = [self.curTask]
        self.prevTask = ()
        self.prevState = []
        self.origin = 0

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

    def stateDictionary(self, task):
        print('current state', task)
        nextTransition = (self.stateConditions[task])
        print('next transition found: ', nextTransition)
        nextState = self.transitions[nextTransition]
        return nextState
    
    def runPIGPS(self):
        while len(self.tasks) > 0:
            print('runGPS loop. Task:', self.tasks)
            nextTask = self.stateDictionary(self.tasks[0]) # fetch next state object
            self.prevTask = self.curTask # backup last task incase of exception
            self.curTask = nextTask      # set curTask as next the next task before attempt to run

            try:
                State = nextTask(self.prevState, self.origin)
                State.run()

                if len(self.tasks) <= 1: # if no other tasks exist add next task
                    self.tasks.append((State.stateName, State.errState)) # use errcode to generate next state
                self.prevState = State     # record most recent state 
                self.origin = State.origin # if state operation deterimines change in location, update controller
                self.tasks.pop(0)
                
            except:
                print('in exception loop', self.curTask)
                isNotRetry = len(self.tasks) == 1
                if isNotRetry:
                    self.curTask = (self.curTask[0], 2)
    
    

