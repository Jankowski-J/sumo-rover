import RPi.GPIO as GPIO                    
import time                                
import sys
GPIO.setmode(GPIO.BOARD)                    
GPIO.setwarnings(False)

class UltrasonicSensor:
  
  def __init__(self, trigPin, echoPin, name="Default"):
    self.triggerPin = trigPin
    self.echoPin = echoPin
    self.name = name

    GPIO.setup(self.triggerPin, GPIO.OUT)
    GPIO.setup(self.echoPin, GPIO.IN)

  def _read(self):
    try:
      GPIO.output(self.triggerPin, GPIO.LOW)
      time.sleep(0.5)
    
      GPIO.output(self.triggerPin, GPIO.HIGH)
      time.sleep(0.00001)
      GPIO.output(self.triggerPin, GPIO.LOW)
   
      pulse_start = 0
      pulse_end = 0

      while GPIO.input(self.echoPin) == 0:
        pulse_start = time.time();

      while GPIO.input(self.echoPin) == 1:
        pulse_end = time.time()

      pulse_duration = pulse_end - pulse_start

      distance = pulse_duration * 17150
      distance = round(distance, 2)

      if distance > 2 and distance <= 200:
        print(self._formattedName(), " Distance:", distance, "cm")
      else:
        print(self._formattedName(), "Out of range")

    except:
      print(self._formattedName(), "Unexpected error:", sys.exc_info()[0])

  def _formattedName(self):
    formatted = "[ UltrasonicSensor: " + self.name + " ]"
    formatted = formatted.ljust(40, ' ')
    return formatted

  def readInLoop(self):
    while True:
      self._read()
