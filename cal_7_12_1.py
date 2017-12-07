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

def regression(x_s,y_s):
 # mean of all elements
 x_mean= 0.1*statistics.mean(x_s)
 y_mean= 0.1*statistics.mean(y_s)

 # square every element
 x2=0.1*0.1*x_s*x_s
 x2_mean = statistics.mean(x2)

 # element wise multiplication of 2 list
 xy=0.1*0.1*x_s*y_s
 xy_mean = statistics.mean(xy)

 # regression calculation
 m = ((x_mean * y_mean) - xy_mean)/((x_mean*x_mean) - x2_mean)
 m=round(m,4)
 c = 10*round(y_mean - (x_mean*m))
 return m,c

 
b=slave_id(1)
print ("Board IDs: "),b
time.sleep(1)


smb = minimalmodbus.Instrument('COM15',b,mode='rtu')
smb.debug= False
meter = minimalmodbus.Instrument('COM16',3,mode='rtu')
meter.debug= False

x = np.zeros((2,3,8))
y = np.zeros((2,3,8))
chx = np.zeros((16,3))
chy = np.zeros((16,3))
m = np.zeros(16)
c = np.zeros(16)

# raw_input("Keep setting A and current 3A and PRESS ENTER")
x[0][0] = smb.read_registers(3,8,3)
y[0][0] = meter.read_registers(3,8,3)
time.sleep(1)

# raw_input("Keep setting B and current 3A and PRESS ENTER")
x[1][0]= smb.read_registers(11,8,3)
y[1][0]= meter.read_registers(3,8,3)
time.sleep(1)

# raw_input("Keep setting B and current 15A and PRESS ENTER")
x[1][1]= smb.read_registers(11,8,3)
y[1][1]= meter.read_registers(3,8,3)
time.sleep(1)

# raw_input("Keep setting A and current 15A and PRESS ENTER")
x[0][1] = smb.read_registers(3,8,3)
y[0][1] = meter.read_registers(3,8,3)
time.sleep(1)

# raw_input("Keep setting A and current 30A and PRESS ENTER")
x[0][2] = smb.read_registers(3,8,3)
y[0][2] = meter.read_registers(3,8,3)
time.sleep(1)

# raw_input("Keep setting B and current 30A and PRESS ENTER")
x[1][2] = smb.read_registers(11,8,3)
y[1][2] = meter.read_registers(3,8,3)
time.sleep(1)

for i in range(0,8):
 chx[i] = x[0][0][i] , x[0][1][i] , x[0][2][i]
 print(" Chx %d"%(i+1)),chx[i]
 chy[i] = y[0][0][i] , y[0][1][i] , y[0][2][i]
 print(" Chy %d"%(i+1)),chy[i]
for i in range(0,8):
 chx[i+8] = x[1][0][i] , x[1][1][i] , x[1][2][i]
 print(" Chx %d"%(i+9)),chx[i]
 chy[i+8] = y[1][0][i] , y[1][1][i] , y[1][2][i]
 print(" Chy %d"%(i+9)),chy[i]
print("Input Done!")

#Regression
for i in range(0,16):
 m[i],c[i] = regression(chx[i],chy[i])
print("Regression Done!")
m = 1000*m
print("m"),m
print("c"),c