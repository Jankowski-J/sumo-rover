import RPi.GPIO as GPIO
import sys

import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

GPIO.output(26, GPIO.HIGH)
GPIO.output(16, GPIO.HIGH)

try:
	print("sanity check running")
	while True:
		time.sleep(1)
		GPIO.output(26, GPIO.LOW)
		time.sleep(1)
		GPIO.output(26, GPIO.HIGH)

except KeyboardInterrupt:
	print("User cancelled")
	GPIO.output(26, GPIO.LOW)
	GPIO.output(16, GPIO.OW)
