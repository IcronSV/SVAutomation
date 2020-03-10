import json
import usb.core

PID = []
VID = []
result = []

with open('./tmp/devices.json') as json_file:
    data = json.load(json_file)

devstr = input('Input the device names as listed in the .json file seperated by commas: ')
devlst = devstr.split(',')
for dev in devlst:
    for x in data:
        if x['Device'] == dev:
            PID.append(x['PID'])
            VID.append(x['VID'])


for i in (0, len(PID)):
    conndev = usb.core.find(idVendor = VID[i-1], idProduct = PID[i-1] )
    if conndev == None:
        result.append(0)
        continue

    for x in data:
        if conndev.speed == x['Speed']:
            result.append(1)
        else:
            result.append(2)

print(result)
                

