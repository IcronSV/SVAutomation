#This script was written by Brendan Murray on 11/03/2020 for Icron Technologies SV automation project
#This script takes an input from user or master host and returns a list corresponding to the csv inputted devices with values
# 0 for failed enum, 1 for pass, 2 for incorrect enum and 3 if the input name was not valid
#Commented out code worked when all inputs were valid
import json
import usb.core

#initialize our lists
PID = []
VID = []
result = []
i=0

#open our .json device list and import the values as a list of lists
with open('./devices.json') as json_file:
    data = json.load(json_file)

#Get user input for the name of the device, this will likely to be changed to take input in some other way from the
#master host
devstr = input('Input the device names exactly as listed in the .json file seperated by commas: ')
#split the input string as if it was a .csv file which is likely how it will be done in the future
devlst = devstr.split(',')

"""for dev in devlst:
    #iterate through each entry in the data (potential to be optimized once the json structure is finalized)
    for x in data:
        #If the json device name == the inputted name, save the PID and VID to search with
        if x['Device'] == dev:
            PID.append(x['PID'])
            VID.append(x['VID'])
            break
del dev"""

while len(PID) < len(devlst):
    PID.append('4')
    VID.append('4')

while True:
    for x in data:
        if x['Device']==devlst[i]:
            PID[i]=(x['PID'])
            VID[i]=(x['VID'])
            break
    i+=1 
    if i > len(devlst)-1:
        break

"""for i in (0, len(PID)-1):
    conndev = usb.core.find(idVendor=int(VID[i], 16), idProduct=int(PID[i], 16))
    if conndev == None:
        result.append(0)
        del conndev
        continue
    if conndev != None:
        for x in data:
            if hex(conndev.speed) == x['Speed']:
                result.append(1)
                del conndev
                break
            else:
                result.append(2)
                del conndev
                break
"""

i=0
while True:
    if PID[i] == '4' and VID[i] == '4':
        result.append(3)
        i+=1
        if len(result) == len(devlst):
            break
        continue
    conndev = usb.core.find(idVendor=int(VID[i], 16), idProduct=int(PID[i], 16))
    if conndev == None:
        result.append(0)
        del conndev
        i+=1
        if len(result) == len(devlst):
            break
        continue
    if conndev != None:
        for x in data:
            if hex(conndev.speed) == x['Speed']:
                result.append(1)
                del conndev
                i+=1
                break
            else:
                result.append(2)
                del conndev
                i+=1
                break
        if len(result) == len(devlst):
            break
        continue
    i+=1
    if len(result) == len(devlst):
        break

print(result)