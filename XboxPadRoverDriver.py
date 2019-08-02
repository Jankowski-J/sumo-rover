from RoverController import RoverController
from XboxController import XboxController
import sys
import time

if __name__ == '__main__':

    # generic call back
    def controlCallBack(xboxControlId, value):
        print "Control Id = {}, Value = {}".format(xboxControlId, value)

    power = 100
    left_power = 100
    right_power = 100

    roverCont = RoverController()


    def go():
        roverCont.go()


    # specific callbacks for the left thumb (X & Y)
    def leftThumbX(xValue):
        is_turning_left = xValue < 0

        decrease = abs(xValue)

        if is_turning_left:
            left_power = 100 - decrease
            right_power = 100
        else:
            right_power = 100 - decrease
            left_power = 100

        roverCont.steer(power, left_power, right_power)

        print "LX {}".format(xValue)


    def leftThumbY(yValue):
        left_power = 100
        right_power = 100
        power = yValue
        roverCont.steer(power, left_power, right_power)
        print "LY {}".format(yValue)


    # setup xbox controller, set out the deadzone and scale, also invert the Y Axis (for some reason in Pygame negative is up - wierd!
    xbox_cont = XboxController(controlCallBack, deadzone=30, scale=100, invertYAxis=True, callback=go)


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
        xbox_cont.stop()
        roverCont.stop()


    # setup the left thumb (X & Y) callbacks
    xbox_cont.setupControlCallback(xbox_cont.XboxControls.LTHUMBX, leftThumbX)
    xbox_cont.setupControlCallback(xbox_cont.XboxControls.LTHUMBY, leftThumbY)
    xbox_cont.setupControlCallback(xbox_cont.XboxControls.A, aBtnCallback)
    xbox_cont.setupControlCallback(xbox_cont.XboxControls.B, bBtnCallback)
    xbox_cont.setupControlCallback(xbox_cont.XboxControls.X, xBtnCallback)
    xbox_cont.setupControlCallback(xbox_cont.XboxControls.Y, yBtnCallback)
    xbox_cont.setupControlCallback(xbox_cont.XboxControls.START, startCallback)
    xbox_cont.setupControlCallback(xbox_cont.XboxControls.BACK, stopCallback)
    xbox_cont.setupControlCallback(xbox_cont.XboxControls.XBOX, exitCallback)


    try:
        # start the controller
        xbox_cont.start()
        print "xbox controller running"
        while True:
            time.sleep(1)

    # Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    # error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    finally:
        # stop the controller
        xbox_cont.stop()
        roverCont.stop()
