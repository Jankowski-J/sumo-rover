import RPi.GPIO as GPIO
import time
from RoverController import RoverController

RoverCont = RoverController(stbyPin=12, leftTopPin=20, leftBotPin=21, leftPowerPin=16, rightTopPin=24,rightBotPin=23, rightPowerPin=18 )
RoverCont.start()

while True:
	RoverCont.goForwards()
	print("going forward")
	time.sleep(1)
	print("going backward")
	RoverCont.goBackwards()
	time.sleep(1)
