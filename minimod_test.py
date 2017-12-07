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

# .read_registers(startingaddress,noofregisters,functioncode)
set1= input('Enter 1st Setting 1 or 2: ')
if set1==1:
 time.sleep(0.5)
 x1smb  =  smb.read_registers(3,8,3)
 print('x1smb: '),x1smb
 time.sleep(0.5)
 y1smb  =  meter.read_registers(3,8,3)
 print('y1smb: '),y1smb
if set1==2:
 time.sleep(0.5)
 x2smb  =  smb.read_registers(11,8,3)
 print('x2smb: '),x2smb
 time.sleep(0.5)
 y2smb  =  meter.read_registers(3,8,3)
 print('y2smb: '),y2smb

set2= input('Enter 2nd Setting 1 or 2: ')
if set2==1:
 time.sleep(0.5)
 x1smb  =  smb.read_registers(3,8,3)
 print('x1smb: '),x1smb
 time.sleep(0.5)
 y1smb  =  meter.read_registers(3,8,3)
 print('y1smb: '),y1smb
if set2==2:
 time.sleep(0.5)
 x2smb  =  smb.read_registers(11,8,3)
 print('x2smb: '),x2smb
 time.sleep(0.5)
 y2smb  =  meter.read_registers(3,8,3)
 print('y2smb: '),y2smb

xsmb = x1smb + x2smb
ysmb = y1smb + y2smb

for i in range(0,16):
 print ('Current of SMB Str  %d: '%(i+1)),xsmb[i]
 print ('Current on meter Ch %d: '%(i+1)),ysmb[i]

#list
xs = np.array(xsmb)
ys = np.array(ysmb)

# mean of all elements
x_mean= 0.1*statistics.mean(xs)
y_mean= 0.1*statistics.mean(ys)

# square every element
x2=0.1*0.1*xs*xs
x2_mean = statistics.mean(x2)

# element wise multiplication of 2 list
xy=0.1*0.1*xs*ys
xy_mean = statistics.mean(xy)

# regression calculation
m = ((x_mean * y_mean) - xy_mean)/((x_mean*x_mean) - x2_mean)
m=round(m,4)
print("m:"),m
c = 10*round(y_mean - (x_mean*m))
print("c:"),c

xs=(xs*m)+c
print("Y:"),ys
xs=map(int, xs)
print("xs:"),xs

# er=xs-ys
# print("error"),er
# erp=er*100/ys
# print("%error"),erp