#This script was written by Brendan Murray on 11/03/2020 for Icron Technologies SV automation project
#This script takes an input from user or master host and returns a list corresponding to the csv inputted devices with values
# 0 for failed enum, 1 for pass, 2 for incorrect enum and 3 if the input name was not valid
#There is a known bug with pyUSB which throws exceptions when deleting instances of the usb class.
#however these do not affect the program functionality and are unavoidable to my knowledge when using pyUSB.

#Commented out code works when all inputs are valid
import json
import usb.core

#initialize certain variables
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

#MODULE 1 replacement (no error check)
"""for dev in devlst:
    #iterate through each entry in the data (potential to be optimized once the json structure is finalized)
    for x in data:
        #If the json device name == the inputted name, save the PID and VID to search with
        if x['Device'] == dev:
            PID.append(x['PID'])
            VID.append(x['VID'])
            break
del dev"""

#MODULE 1
#Creating a "could not lookup" value for the PID and VID that will be used when it can't be found in the json
while len(PID) < len(devlst):
    PID.append('3')
    VID.append('3')
#Loop to lookup the PID and VID of our devices
while True:
    for x in data:
        if x['Device']==devlst[i]:
            PID[i]=(x['PID'])
            VID[i]=(x['VID'])
            break
    i+=1 
    if i > len(devlst)-1:
        break

#MODULE 2 Replacement (no error check)
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

#Resetting our iterator i
i=0
#Loop to fill our result list with the correct values MODULE 2
while True:
    #If the PID and VID are still set to their "could not lookup" error values, set that as the result
    if PID[i] == '3' and VID[i] == '3':
        result.append(3)
        #this block incrememnts our iterator and checks if we should break from the loop (if we have filled the results)
        i+=1
        if len(result) == len(devlst):
            break
        continue
    #Since we were able to lookup the PID and VID, we use it to try and find the device through pyUSB
    #This function would only take the PID and VID as integers, not their hex strings
    conndev = usb.core.find(idVendor=int(VID[i], 16), idProduct=int(PID[i], 16))
    #If we did not find the device the function returns None, which we fill a 0 into result for
    if conndev == None:
        result.append(0)
        del conndev
        i+=1
        if len(result) == len(devlst):
            break
        continue
    #If the result is not none, it found a device. We check its speed against the JSON table
    #If it is the correct speed, write 1 to the results. If it is incorrect write 2 to the results
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
#Finally, print the result, for ease of testing
print(result)