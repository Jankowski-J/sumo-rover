from USSensorManager import UltrasonicSensorsManager

manager = UltrasonicSensorsManager()

manager.addSensor("bottom", 40, 38)
manager.addSensor("top", 37, 35)


manager.beginReadFromSensors()
