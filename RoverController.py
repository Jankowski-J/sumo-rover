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
    
    def __init__(self, stbyPin=13, leftTopPin=8, leftBotPin=10,
	leftPowerPin=11, rightTopPin=5, rightBotPin=7, rightPowerPin=12):
	self.stbyPin = stbyPin

	self.leftTopPin = leftTopPin
	self.leftBotPin = leftBotPin
	self.leftPowerPin = leftPowerPin

	self.rightTopPin = rightTopPin
	self.rightBotPin = rightBotPin
	self.rightPowerPin = rightPowerPin

	GPIO.setup(self.stbyPin, GPIO.OUT)

	GPIO.setup(self.leftTopPin, GPIO.OUT)
	GPIO.setup(self.leftBotPin, GPIO.OUT)
	GPIO.setup(self.leftPowerPin, GPIO.OUT)

	GPIO.setup(self.rightTopPin, GPIO.OUT)
	GPIO.setup(self.rightBotPin, GPIO.OUT)
	GPIO.setup(self.rightPowerPin, GPIO.OUT)

	GPIO.output(self.stbyPin, GPIO.LOW)

	self.leftTopPinValue = GPIO.HIGH
	GPIO.output(self.leftTopPin, self.leftTopPinValue)
	self.leftBotPinValue = GPIO.HIGH
	GPIO.output(self.leftBotPin, self.leftBotPinValue)
	self.leftPower = GPIO.PWM(self.leftPowerPin, 50)
	
	self.rightTopPinValue = GPIO.HIGH
	GPIO.output(self.rightTopPin, self.rightTopPinValue)
	self.rightBotPinValue = GPIO.HIGH
	GPIO.output(self.rightBotPin, self.rightBotPinValue)
	self.rightPower = GPIO.PWM(self.rightPowerPin, 50)

    LOW_POWER_LEVEL = 40
    HIGH_POWER_LEVEL = 100

    def start(self):
        GPIO.output(self.stbyPin, GPIO.HIGH)
	self.leftPower.start(RoverController.HIGH_POWER_LEVEL)
	self.rightPower.start(RoverController.HIGH_POWER_LEVEL)
        self.goForwards()

    def _writeOutputs(self):
        print(self.leftTopPinValue, self.leftBotPinValue, self.rightTopPinValue, self.rightBotPinValue)
        GPIO.output(self.leftTopPin, self.leftTopPinValue)
        GPIO.output(self.leftBotPin, self.leftBotPinValue)
        GPIO.output(self.rightTopPin, self.rightTopPinValue)
        GPIO.output(self.rightBotPin, self.rightBotPinValue)
	
    def _hardStop(self):
        self.leftTopPinValue = GPIO.HIGH
        self.leftBotPinValue = GPIO.HIGH
        self.rightTopPinValue = GPIO.HIGH
        self.rightBotPinValue = GPIO.HIGH

    def _stopLeftEngine(self):
        self.leftTopPinValue = GPIO.HIGH
        self.leftBotPinValue = GPIO.HIGH

    def _stopRightEngine(self):
        self.rightTopPinValue = GPIO.HIGH
        self.rightBotPinValue = GPIO.HIGH

    def _spinLeftEngineClockwise(self):
        self.leftTopPinValue = GPIO.HIGH
        self.leftBotPinValue = GPIO.LOW

    def _spinLeftEngineCounterClockwise(self):
        self.leftTopPinValue = GPIO.LOW
        self.leftBotPinValue = GPIO.HIGH

    def _spinRightEngineClockwise(self):
        self.rightTopPinValue = GPIO.HIGH
        self.rightBotPinValue = GPIO.LOW

    def _spinRightEngineCounterClockwise(self):
        self.rightTopPinValue = GPIO.LOW
        self.rightBotPinValue = GPIO.HIGH

    def _toggleLeftEnginePower(self, fullPower = True):
	if fullPower:
	    self.leftPower.ChangeDutyCycle(RoverController.HIGH_POWER_LEVEL)
	else:
	    self.leftPower.ChangeDutyCycle(RoverController.LOW_POWER_LEVEL)

    def _toggleRightEnginePower(self, fullPower = True):
	if fullPower:
	    self.rightPower.ChangeDutyCycle(RoverController.HIGH_POWER_LEVEL)
	else:
	    self.rightPower.ChangeDutyCycle(RoverController.LOW_POWER_LEVEL)

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
