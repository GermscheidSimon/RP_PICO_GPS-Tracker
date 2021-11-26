from ConcreteStates import *;
from fsm_concept import PIGPS;

class ConcreteState_MockObjs():
    
    def READGPS_SuccessPath(self):
        testGPSREAD = ReadingGPS()
        testGPSREAD.data = [
            ((10),(10),('time'),('date'))
        ]
        return testGPSREAD

    def READGPS_EXCEPTIONTHROWN(self):
        testGPSREAD = ReadingGPS()
        testGPSREAD.errState = 2
        testGPSREAD.data = []
        return testGPSREAD
        

class ConcreteStates_IntegrationTests(object):
    
    def __init__(self):
        self._pigps = PIGPS()
    
    def run_READGPS_loop_test(self):
        self._pigps.runPIGPS()

def runTessts():
    test = ConcreteStates_IntegrationTests()
    test.run_READGPS_loop_test()
runTessts()
