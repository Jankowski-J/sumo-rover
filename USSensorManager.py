from UltrasonicSensor import UltrasonicSensor
from threading import Thread

class UltrasonicSensorsManager:

  def __init__(self):
    self.sensors = list()

  def addSensor(self, name, triggerPin, echoPin):
    sensor = UltrasonicSensor(triggerPin, echoPin, name)
    self.sensors.append(sensor)

  def beginReadFromSensors(self):
    threads = [Thread(target=x.readInLoop) for x in self.sensors]
    for thread in threads:
      thread.start()

