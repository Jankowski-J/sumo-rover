import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.output(5, GPIO.HIGH)
GPIO.output(7, GPIO.LOW)
GPIO.output(8, GPIO.HIGH)
GPIO.output(10, GPIO.LOW)
GPIO.setup(11, GPIO.OUT)

class RoverController():
    
    def __init__(self, stbyPin=13):
	self.stbyPin = stbyPin
	GPIO.setup(self.stbyPin, GPIO.OUT)
	GPIO.output(self.stbyPin, GPIO.LOW)

    leftPinTop = 8
    leftPinTopValue = GPIO.HIGH
    leftPinBot = 10
    leftPinBotValue = GPIO.HIGH

    leftPowerPin = 11
    leftPower = GPIO.PWM(11, 50)
    leftPower.start(100)

    rightPinTop = 5
    rightPinTopValue = GPIO.HIGH
    rightPinBot = 7
    rightPinBotValue = GPIO.HIGH

    rightPowerPin = 12
    rightPower = GPIO.PWM(12, 50)
    rightPower.start(100)

    lowPowerLevel = 55

    def start(self):
        GPIO.output(self.stbyPin, GPIO.HIGH)
        self.goForwards()

    def _writeOutputs(self):
        print(self.leftPinTopValue, self.leftPinBotValue, self.rightPinTopValue, self.rightPinBotValue)
        GPIO.output(self.leftPinTop, self.leftPinTopValue)
        GPIO.output(self.leftPinBot, self.leftPinBotValue)
        GPIO.output(self.rightPinTop, self.rightPinTopValue)
        GPIO.output(self.rightPinBot, self.rightPinBotValue)
	
    def _hardStop(self):
        self.leftPinTopValue = GPIO.HIGH
        self.leftPinBotValue = GPIO.HIGH
        self.rightPinTopValue = GPIO.HIGH
        self.rightPinBotValue = GPIO.HIGH

    def _stopLeftEngine(self):
        self.leftPinTopValue = GPIO.HIGH
        self.leftPinBotValue = GPIO.HIGH

    def _stopRightEngine(self):
        self.rightPinTopValue = GPIO.HIGH
        self.rightPinBotValue = GPIO.HIGH

    def _spinLeftEngineClockwise(self):
        self.leftPinTopValue = GPIO.HIGH
        self.leftPinBotValue = GPIO.LOW

    def _spinLeftEngineCounterClockwise(self):
        self.leftPinTopValue = GPIO.LOW
        self.leftPinBotValue = GPIO.HIGH

    def _spinRightEngineClockwise(self):
        self.rightPinTopValue = GPIO.HIGH
        self.rightPinBotValue = GPIO.LOW

    def _spinRightEngineCounterClockwise(self):
        self.rightPinTopValue = GPIO.LOW
        self.rightPinBotValue = GPIO.HIGH

    def _toggleLeftEnginePower(self, fullPower = True):
	if fullPower:
	    self.leftPower.ChangeDutyCycle(100)
	else:
	    self.leftPower.ChangeDutyCycle(self.lowPowerLevel)

    def _toggleRightEnginePower(self, fullPower = True):
	if fullPower:
	    self.rightPower.ChangeDutyCycle(100)
	else:
	    self.rightPower.ChangeDutyCycle(self.lowPowerLevel)

    def goForwards(self):
        self._spinLeftEngineClockwise()
        self._toggleLeftEnginePower(True)
        self._spinRightEngineClockwise()
        self._toggleRightEnginePower(True)
        self.go()

    def goBackwards(self):
        self._spinLeftEngineCounterClockwise()
        self._toggleLeftEnginePower(True)
        self._spinRightEngineCounterClockwise()
        self._toggleRightEnginePower(True)
        self.go()

    def go(self):
        self._writeOutputs()

    def turnRight(self):
        self._toggleLeftEnginePower(True)
        self._toggleRightEnginePower(False)
        self.go()
   
    def turnLeft(self):
        self._toggleLeftEnginePower(False)
        self._toggleRightEnginePower(True)
        self.go()
	
    def stop(self):
        self._hardStop()
        self._writeOutputs()	