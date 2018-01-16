from constants import *

class importData:

    sensors = []

    def __init__(self, fileName, numberOfTrays):
        newLines = [line.rstrip('\n') for line in open(fileName)]
        sampleNumber = 0
        sensorType = TEMPERATURE #The data is stored such that the first 'numberOfTrays' values contain temperature data

        ListOfLists = []
        for line in newLines:
            ListOfLists.append(line.split(','))

        while ListOfLists:
            tempList = []
            channel = 0
            for line in ListOfLists:
                tempList.append(float(line.pop(0)))
                channel = line.pop(0)
            channel = int(float(channel))
            if (sampleNumber >= numberOfTrays): #This ensures the first 'numberOfTrays' sensors are recorded as temp
                sensorType = PELTIER
            sampleNumber = sampleNumber + 1
            self.sensors.append(sensor(channel,sensorType,tempList))
            if not line:
                break

    def ConvertTemperatures(self):
        for device in self.sensors:
            if device.type == TEMPERATURE:
                for index, resistance in enumerate(device.samples):
                    device.samples[index] = (-0.007742 * resistance + 106.5)



class sensor:
    id = None
    trayNumber = None
    type = UNKNOWN_UNINITIALIZED
    samples = []

    def __init__(self, idNumber,trayNo,typeOfSensor,values):
        self.id = idNumber
        self.trayNumber = trayNo
        self.type = typeOfSensor
        self.samples = values

    def __repr__(self):
        return "#" + str(self.id) + "-" + str(self.samples)

class trayOfSensors:
    temperatureSensor = None
    otherSensorsInTray = []






data = importData('test.txt',6)
print(data.sensors)
data.ConvertTemperatures()
print(data.sensors)






