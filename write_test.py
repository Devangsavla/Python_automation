import minimalmodbus
import serial
import time

#Define Communication parameters
minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1
#not closing port after each call causes buffer overflow issue(Probably?)
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

smb = minimalmodbus.Instrument('COM15',5,mode='rtu')
smb.debug= True

for i in range(1,17):
 smb.write_register(i, 1000, 0)
 print("Write to %d done"%i)
 time.sleep(0.2)
for i in range(17,33):
 smb.write_register(i, 400, 0)
  print("Write to %d done"%i)
 time.sleep(0.2)
smb.write_register(33, 1000, 0)
time.sleep(0.2)
smb.write_register(34, 400, 0)
time.sleep(0.2) 
print("writing done")

x = np.zeros((2,3,8))
y = np.zeros((2,3,8))
chx = np.zeros((16,3))
chy = np.zeros((16,3))
m = np.zeros(16)
c = np.zeros(16)

raw_input("Keep setting A and current 3A and PRESS ENTER")
x[0][0] = smb.read_registers(3,8,3)
y[0][0] = meter.read_registers(3,8,3)
time.sleep(1)

raw_input("Keep setting B and current 3A and PRESS ENTER")
x[1][0]= smb.read_registers(11,8,3)
y[1][0]= meter.read_registers(3,8,3)
time.sleep(1)

raw_input("Keep setting B and current 15A and PRESS ENTER")
x[1][1]= smb.read_registers(11,8,3)
y[1][1]= meter.read_registers(3,8,3)
time.sleep(1)

raw_input("Keep setting A and current 15A and PRESS ENTER")
x[0][1] = smb.read_registers(3,8,3)
y[0][1] = meter.read_registers(3,8,3)
time.sleep(1)

raw_input("Keep setting A and current 30A and PRESS ENTER")
x[0][2] = smb.read_registers(3,8,3)
y[0][2] = meter.read_registers(3,8,3)
time.sleep(1)

raw_input("Keep setting B and current 30A and PRESS ENTER")
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