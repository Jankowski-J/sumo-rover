from UltrasonicSensor import UltrasonicSensor
import time
from threading import Thread

class UltrasonicSensorsManager:

  def __init__(self):
    self.sensors = list()

  def addSensor(self, name, triggerPin, echoPin):
    sensor = UltrasonicSensor(triggerPin, echoPin, name)
    self.sensors.append(sensor)

  def beginReadFromSensors(self):
    threads = [Thread(target=x.readInLoop, name=x.getName()) for x in self.sensors]
    for thread in threads:
      thread.start()
 
    while True:
      time.sleep(5)
      print("In reading loop. Threads:", len(threads))

      for t in threads:
        print(t.name, " | is alive?", t.isAlive())

