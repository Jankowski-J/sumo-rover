from RoverController import RoverController
from XboxController import XboxController
import sys
import time

if __name__ == '__main__':
    
    #generic call back
    def controlCallBack(xboxControlId, value):
        print "Control Id = {}, Value = {}".format(xboxControlId, value)

    roverCont = RoverController()
       
    def go():
	roverCont.go()

    #specific callbacks for the left thumb (X & Y)
    def leftThumbX(xValue):
        print "LX {}".format(xValue)
    def leftThumbY(yValue):
        print "LY {}".format(yValue)

    #setup xbox controller, set out the deadzone and scale, also invert the Y Axis (for some reason in Pygame negative is up - wierd! 
    xboxCont = XboxController(controlCallBack, deadzone = 30, scale = 100, invertYAxis = True, callback = go)

    def aBtnCallback(id):
        roverCont.goBackwards()

    def bBtnCallback(id):
	print("turning right")
        roverCont.turnRight()

    def xBtnCallback(id):
	print("turning left")
	roverCont.turnLeft()
	
    def yBtnCallback(id):
        roverCont.goForwards()

    def startCallback(id):
	roverCont.start()

    def stopCallback(id):
	roverCont.stop()
        
    def goCallback(id):
	roverCont.goForwards()

    def exitCallback(id):
	xboxCont.stop()
	roverCont.stop()
    
    #setup the left thumb (X & Y) callbacks
    xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBX, leftThumbX)
    xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBY, leftThumbY)
    xboxCont.setupControlCallback(xboxCont.XboxControls.A, aBtnCallback)
    xboxCont.setupControlCallback(xboxCont.XboxControls.B, bBtnCallback)
    xboxCont.setupControlCallback(xboxCont.XboxControls.X, xBtnCallback)
    xboxCont.setupControlCallback(xboxCont.XboxControls.Y, yBtnCallback)
    xboxCont.setupControlCallback(xboxCont.XboxControls.START, startCallback)
    xboxCont.setupControlCallback(xboxCont.XboxControls.BACK, stopCallback)
    xboxCont.setupControlCallback(xboxCont.XboxControls.XBOX, exitCallback)
    
    try:
        #start the controller
        xboxCont.start()
        print "xbox controller running"
        while True:
            time.sleep(1)
            
    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"
    
    #error        
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
        
    finally:
        #stop the controller
	xboxCont.stop()
	roverCont.stop()
