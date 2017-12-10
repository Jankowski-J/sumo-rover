from RoverController import RoverController
from console_controller import WsadController
import sys

if __name__ == '__main__':
    
    roverCont = RoverController()
       
    def go():
	roverCont.go()

    def aBtnCallback(id):
        roverCont.goBackwards()

    def bBtnCallback(id):
        roverCont.turnRight()

    def xBtnCallback(id):
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

    wsad = WsadController(w=(lambda: roverController.goForwards())
   
    try:
        #start the controller
        wsad.start()
        print "keyboard controller running"
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
	roverCont.stop()
