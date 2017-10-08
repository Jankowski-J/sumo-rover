import time
from RoverController import RoverController

RoverCont = RoverController(stbyPin=12, leftTopPin=24, leftBotPin=23, leftPowerPin=18, rightTopPin=20, rightBotPin=21, rightPowerPin=16)
RoverCont.start()

try:
	while True:
		print("CURSES:", derp)
		RoverCont.goForwards()
		print("going forward")
		time.sleep(1)
		print("going backward")
		RoverCont.goBackwards()
		time.sleep(1)	

except KeyboardInterrupt:
	print("User cancelled")

finally:
	RoverCont.stop()
