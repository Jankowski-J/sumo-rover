import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

'''
    This class is used to control a two-motor rover, 
    which has tracks. It is assumed, that it uses a Pololu controller.
'''


class RoverController():
    """
        Constructor paramaters:
        stbyPin - board number of STBY pin, which turns the Pololu controller on/off
        leftTopPin, leftBotPin - left engine inputs
        leftPowerPin - through this pin, a PWM signal for left engine is outputted
        rightTopPin, rightBotPin - right engine inputs
        rightPowerPin - through this pin, a PWM signal for right engine is outputted
    """

    def __init__(self, stbyPin=12, leftTopPin=24, leftBotPin=23,
                 leftPowerPin=18, rightTopPin=20, rightBotPin=21, rightPowerPin=16):
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
        self.left_engine = GPIO.PWM(self.leftPowerPin, 50)

        self.rightTopPinValue = GPIO.HIGH
        GPIO.output(self.rightTopPin, self.rightTopPinValue)
        self.rightBotPinValue = GPIO.HIGH
        GPIO.output(self.rightBotPin, self.rightBotPinValue)
        self.right_engine = GPIO.PWM(self.rightPowerPin, 50)

    LOW_POWER_LEVEL = 25
    HIGH_POWER_LEVEL = 60

    def start(self):
        GPIO.output(self.stbyPin, GPIO.HIGH)
        self.left_engine.start(RoverController.HIGH_POWER_LEVEL)
        self.right_engine.start(RoverController.HIGH_POWER_LEVEL)
        self.goForwards()

    def _writeOutputs(self):
        # print(self.leftTopPinValue, self.leftBotPinValue, self.rightTopPinValue, self.rightBotPinValue)
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

    def _toggleLeftEnginePower(self, fullPower=True):
        if fullPower:
            self.left_engine.ChangeDutyCycle(RoverController.HIGH_POWER_LEVEL)
        else:
            self.left_engine.ChangeDutyCycle(RoverController.LOW_POWER_LEVEL)

    def _toggleRightEnginePower(self, fullPower=True):
        if fullPower:
            self.right_engine.ChangeDutyCycle(RoverController.HIGH_POWER_LEVEL)
        else:
            self.right_engine.ChangeDutyCycle(RoverController.LOW_POWER_LEVEL)

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

    def _rev_left_engine(self, max_power_level=100):
        power_level = RoverController.HIGH_POWER_LEVEL * max_power_level / 100
        self.left_engine.ChangeDutyCycle(power_level)

    def _rev_right_engine(self, max_power_level=100):
        power_level = RoverController.HIGH_POWER_LEVEL * max_power_level / 100
        self.right_engine.ChangeDutyCycle(power_level)

    @staticmethod
    def normalize_power(power):
        if power > 100:
            power = 100
        if power < 0:
            power = 0

        return power

    def steer(self, power=100, left_power=100, right_power=100):
        if power > 0:
            self._spinLeftEngineClockwise()
            self._spinRightEngineClockwise()
        else:
            self._spinLeftEngineCounterClockwise()
            self._spinRightEngineCounterClockwise()

        power = RoverController.normalize_power(power)
        left_power = RoverController.normalize_power(left_power)
        right_power = RoverController.normalize_power(right_power)

        left_power = left_power * power / 100
        right_power = right_power * power / 100

        self._rev_left_engine(left_power)
        self._rev_right_engine(right_power)

        self._writeOutputs()
