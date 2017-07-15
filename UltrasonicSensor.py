import RPi.GPIO as GPIO                    
import time                                
GPIO.setmode(GPIO.BOARD)                    

class UltrasonicSensor:
  
  def __init__(self, trigPin, echoPin):
    self.triggerPin = trigPin
    self.echoPin = echoPin

    GPIO.setup(self.triggerPin, GPIO.OUT)
    GPIO.setup(self.echoPin, GPIO.IN)

  def _read(self):
    GPIO.output(self.triggerPin, GPIO.LOW)
    print("Waiting for sensor to settle")
    time.sleep(0.5)
    
    GPIO.output(self.triggerPin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(self.triggerPin, GPIO.LOW)

    while GPIO.input(self.echoPin) == 0:
      pulse_start = time.time();

    while GPIO.input(self.echoPin) == 1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance, 2)

    if distance > 2 and distance <= 200:
      print("Distance: ", distance, " cm")
    else:
      print("Out of range (", distance, " cm)")

  def readInLoop(self):
    while True:
      self._read()


sensor = UltrasonicSensor(40, 38)
sensor.readInLoop()
