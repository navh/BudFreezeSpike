from constants import *
import numpy as np

class importData:

    def __init__(self, fileName, numberOfTrays, numberOfSensorsPerTray):
        self.totalTrays = numberOfTrays
        self.sensors = []
        self.sensorsPerTray = numberOfSensorsPerTray
        newLines = [line.rstrip('\n') for line in open(fileName)]
        sampleNumber = 0

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

            #The following assumes the first few trays will be a temperature sensor each from a different tray
            #It then assigns the remaining sensors tray numbers in ascending order starting at 0
            #The use of sensorsPerTray-1 is because this number includes one temperature sensor that should already be accounted for

            #Ideally this will leave the sensors with labels in the following order assuming 6 trays of 10 sensors
            # 012345000000000111111111222222222333333333444444444555555555

            if (sampleNumber >= self.totalTrays):
                trayNumber = int((sampleNumber - self.totalTrays)/(self.sensorsPerTray - 1))
                self.sensors.append(sensor(channel, trayNumber, PELTIER, tempList))
            else:
                self.sensors.append(sensor(channel,sampleNumber, TEMPERATURE, tempList))

            sampleNumber = sampleNumber + 1

            #My list does not fail the while loop's test when it's empty...
            if not line:
                break

    def ConvertTemperatures(self):
        for device in self.sensors:
            if device.type == TEMPERATURE:
                for index, resistance in enumerate(device.samples):

                    #This formula was provided by BrockU and assumes a linear relationship between sensor reading and temperature
                    device.samples[index] = (-0.007742 * resistance + 106.5)

    def samplesInTray(self,number):
        justOneTray = []
        for device in self.sensors:
            if device.trayNumber == number:
                justOneTray.append(device)
        return justOneTray




class sensor:

    def __init__(self, idNumber,trayNo,typeOfSensor,values):
        self.id = idNumber
        self.trayNumber = trayNo
        self.type = typeOfSensor
        self.samples = values

    def __repr__(self):
        return "#" + str(self.id) + "-" + str(self.samples)

class trayOfSensors:

    # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2631518/ is how I hope to find spikes


    def __init__(self, sensors):
        self.trayID = sensors[0].id
        self.tempReadings = []
        self.voltReadings = []
        self.tempReadings = list(sensors[0].samples)
        for sens in sensors[1:]:
            self.voltReadings.append(list(sens.samples))


    #This deletes all temperatures above a max, or all temperatures below a min
    def maxMinTemperature(self,temperatureCutoff, trueForMax):
        volts = np.array(self.voltReadings)
        temps = np.array(self.tempReadings)
        print(volts.shape)
        print(volts)
        print(temps)
        for i in reversed(range(len(temps))): #By going backwards indicies that are removed don't matter any more
            if (trueForMax and temps[i] > temperatureCutoff or (not trueForMax) and temps[i] < temperatureCutoff):
                volts = np.delete(volts,i,1)
                temps = np.delete(temps,i)
        self.voltReadings = volts.tolist()
        self.tempReadings = temps.tolist()




data = importData('test.txt',6,10)
print(data.sensors)
data.ConvertTemperatures()
print(data.sensors)

justTestingOneTray = trayOfSensors(data.samplesInTray(2))
justTestingOneTray.maxMinTemperature(3.785,False)









