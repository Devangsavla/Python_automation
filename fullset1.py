import minimalmodbus
import serial
import time
import numpy as np
import statistics

#Define Communication parameters
minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1
#not closing port after each call causes buffer overflow issue(Probably?)
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

def slave_id(a):
 x = input('Enter Slave ID of board %d: ' %a)
 if x not in range(1,20):
  print("Invalid Input. Try again: ")
  slave_id(a)
 return x
 
b=slave_id(1)
print ("Board IDs: "),b
time.sleep(1)

smb = minimalmodbus.Instrument('COM15',b,mode='rtu')
smb.debug= False
meter = minimalmodbus.Instrument('COM16',3,mode='rtu')
meter.debug= False

raw_input("Keep setting A and current 3A and PRESS ENTER")
time.sleep(1)
x11smb  = smb.read_registers(3,8,3)
y11smb  = meter.read_registers(3,8,3)

print ("x11smb"),x11smb
print ("y11smb"),y11smb
time.sleep(1)

raw_input("Keep setting B and current 3A and PRESS ENTER")
x21smb  = smb.read_registers(11,8,3)
y21smb  = meter.read_registers(3,8,3)
print ("x21smb"),x21smb
print ("y21smb"),y21smb
time.sleep(1)

raw_input("Keep setting B and current 15A and PRESS ENTER")
x22smb  = smb.read_registers(11,8,3)
y22smb  = meter.read_registers(3,8,3)
print ("x22smb"),x22smb
print ("y22smb"),y22smb
time.sleep(1)

raw_input("Keep setting A and current 15A and PRESS ENTER")
x12smb  = smb.read_registers(3,8,3)
y12smb  = meter.read_registers(3,8,3)
print ("x12smb"),x12smb
print ("y12smb"),y12smb
time.sleep(1)

raw_input("Keep setting A and current 30A and PRESS ENTER")
x13smb  = smb.read_registers(3,8,3)
y13smb  = meter.read_registers(3,8,3)
print ("x13smb"),x13smb
print ("y13smb"),y13smb
time.sleep(1)

raw_input("Keep setting B and current 30A and PRESS ENTER")
x23smb  = smb.read_registers(11,8,3)
y23smb  = meter.read_registers(3,8,3)
print ("x23smb"),x23smb
print ("y23smb"),y23smb
time.sleep(1)

#merge data of setting A and B as per current setting
x1smb = x11smb + x21smb
x2smb = x12smb + x22smb
x3smb = x13smb + x23smb
y1smb = y11smb + y21smb
y2smb = y12smb + y22smb
y3smb = y13smb + y23smb
print("Reading at 3A"),x1smb
print("Meter at 3A"),y1smb
print("Reading at 15A"),x2smb
print("Meter at 15A"),y2smb
print("Reading at 30A"),x3smb
print("Meter at 30A"),y3smb


#Sort data as per channel
xs1 = (x1smb[0],x2smb[0],x3smb[0])
print("Reading for Channel 1"),xs1
ys1 = (y1smb[0],y2smb[0],y3smb[0])
print("Meter for Channel 1"),ys1

xs2 = (x1smb[1],x2smb[1],x3smb[1])
print("Reading for Channel 2"),xs2
ys2 = (y1smb[1],y2smb[1],y3smb[1])
print("Meter for Channel 2"),ys2

xs3 = (x1smb[2],x2smb[2],x3smb[2])
print("Reading for Channel 3"),xs3
ys3 = (y1smb[2],y2smb[2],y3smb[2])
print("Meter for Channel 3"),ys3

xs4 = (x1smb[3],x2smb[3],x3smb[3])
print("Reading for Channel 4"),xs4
ys4 = (y1smb[3],y2smb[3],y3smb[3])
print("Meter for Channel 4"),ys4

xs5 = (x1smb[4],x2smb[4],x3smb[4])
print("Reading for Channel 5"),xs5
ys5 = (y1smb[4],y2smb[4],y3smb[4])
print("Meter for Channel 5"),ys5

xs6 = (x1smb[5],x2smb[5],x3smb[5])
print("Reading for Channel 6"),xs6
ys6 = (y1smb[5],y2smb[5],y3smb[5])
print("Meter for Channel 6"),ys6

xs7 = (x1smb[6],x2smb[6],x3smb[6])
print("Reading for Channel 7"),xs7
ys7 = (y1smb[6],y2smb[6],y3smb[6])
print("Meter for Channel 7"),ys7

xs8 = (x1smb[7],x2smb[7],x3smb[7])
print("Reading for Channel 8"),xs8
ys8 = (y1smb[7],y2smb[7],y3smb[7])
print("Meter for Channel 8"),ys8

xs9 = (x1smb[8],x2smb[8],x3smb[8])
print("Reading for Channel 9"),xs9
ys9 = (y1smb[8],y2smb[8],y3smb[8])
print("Meter for Channel 9"),ys9

xs10 = (x1smb[9],x2smb[9],x3smb[9])
print("Reading for Channel 10"),xs10
ys10 = (y1smb[9],y2smb[9],y3smb[9])
print("Meter for Channel 10"),ys10

xs11 = (x1smb[10],x2smb[10],x3smb[10])
print("Reading for Channel 11"),xs11
ys11 = (y1smb[10],y2smb[10],y3smb[10])
print("Meter for Channel 11"),ys11

xs12 = (x1smb[11],x2smb[11],x3smb[11])
print("Reading for Channel 12"),xs12
ys12 = (y1smb[11],y2smb[11],y3smb[11])
print("Meter for Channel 12"),ys12

xs13 = (x1smb[12],x2smb[12],x3smb[12])
print("Reading for Channel 13"),xs13
ys13 = (y1smb[12],y2smb[12],y3smb[12])
print("Meter for Channel 13"),ys13

xs14 = (x1smb[13],x2smb[13],x3smb[13])
print("Reading for Channel 14"),xs14
ys14 = (y1smb[13],y2smb[13],y3smb[13])
print("Meter for Channel 14"),ys14

xs15 = (x1smb[14],x2smb[14],x3smb[14])
print("Reading for Channel 15"),xs15
ys15 = (y1smb[14],y2smb[14],y3smb[14])
print("Meter for Channel 15"),ys15

xs16 = (x1smb[15],x2smb[15],x3smb[15])
print("Reading for Channel 16"),xs16
ys16 = (y1smb[15],y2smb[15],y3smb[15])
print("Meter for Channel 16"),ys16

#Regression
