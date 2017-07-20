from USSensorManager import UltrasonicSensorsManager

manager = UltrasonicSensorsManager()

manager.addSensor("left", 40, 38)
manager.addSensor("right", 37, 35)
manager.addSensor("back", 32, 31)

manager.beginReadFromSensors()
