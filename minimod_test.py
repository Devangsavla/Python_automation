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

def slave_id(a):
 x = input('Enter Slave ID of board %d: ' %a)
 if x not in range(1,20):
  print("Invalid Input. Try again: ")
  slave_id(a)
 return x

b=slave_id(1)

print ("Board IDs: "),b
time.sleep(2)

# ch = string_id()
# print ("Channel number: "),ch

smb = minimalmodbus.Instrument('COM15',b,mode='rtu')
smb.debug= False

meter = minimalmodbus.Instrument('COM16',3,mode='rtu')
meter.debug= False

# .read_registers(startingaddress,noofregisters,functioncode)
time.sleep(1)
xsmb  =  smb.read_registers(3,16,3)
time.sleep(1)
ysmb  =  meter.read_registers(3,16,3)

for i in range(0,16):
 print ('Current of String %d: ' %(i+1)),xsmb[i]
 print ('Current on meter channel %d: ' %(i+1)),ysmb[i]
 time.sleep(0.2)

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
print("xs"),xs

# er=xs-ys
# print("error"),er
# erp=er*100/ys
# print("%error"),erp