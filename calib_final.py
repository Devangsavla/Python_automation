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

db = input('Enter Daughter Board Number: ')
mb = input('Enter Mother Board Number: ')
s = input('Enter Slave ID: ')

smb = minimalmodbus.Instrument('COM15',s,mode='rtu')
smb.debug= False

target = open("log_calib.csv","a")

m = np.zeros(16)
c = np.zeros(16)
x = np.zeros(16)
y = np.zeros(16)
d = np.zeros(16)

raw_input("PRESS ENTER to read >")
time.sleep(1)

m = smb.read_registers(0,16,3)
print("M: "),m

c = smb.read_registers(16,16,3)
print("C: "),c

for i in range(0,8):
 raw_input("Keep Setting A and current 3A and PRESS ENTER")
 time.sleep(10)
 
 y[i] = raw_input("Enter multimeter value for Channel %d : "%(i+1))
 x[i] = smb.read_registers((i+1),1,4)
 d[i] = 10*round((y[i]-x[i])/10)
 c[i] = int(c[i]-d[i])

for i in range(8,8):
 raw_input("Keep Setting B and current 3A and PRESS ENTER")
 time.sleep(10)
 
 y[i] = raw_input("Enter multimeter value for Channel %d : "%(i+1))
 x[i] = smb.read_registers((i+1),1,4)
 d[i] = 10*round((y[i]-x[i])/10)
 c[i] = int(c[i]-d[i])

print("Modified C: "),c

vm=smb.read_registers(32,1,4)
vc=smb.read_registers(33,1,4)

raw_input("All OK to write then PRESS ENTER")
smb.write_registers(0,[m[0],m[1],m[2],m[3],m[4],m[5],m[6],m[7],m[8],m[9],m[10],m[11],m[12],m[13],m[14],m[15],c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[12],c[13],c[14],c[15]])

raw_input("Change Complete. Press Enter to record in Excel")
time.sleep(1)

target.write('\n')
target.write("Daughter Board ID")
target.write(",")
target.write("Mother Board ID")
target.write(",")
target.write("Slave ID")
target.write('\n')

target.write(str(db))
target.write(",")
target.write(str(mb))
target.write(",")
target.write(str(s))
target.write('\n')

target.write("Channel Number")
target.write(",")
target.write(str(1))
target.write(",")
target.write(str(2))
target.write(",")
target.write(str(3))
target.write(",")
target.write(str(4))
target.write(",")
target.write(str(5))
target.write(",")
target.write(str(6))
target.write(",")
target.write(str(7))
target.write(",")
target.write(str(8))
target.write(",")
target.write(str(9))
target.write(",")
target.write(str(10))
target.write(",")
target.write(str(11))
target.write(",")
target.write(str(12))
target.write(",")
target.write(str(13))
target.write(",")
target.write(str(14))
target.write(",")
target.write(str(15))
target.write(",")
target.write(str(16))
target.write('\n')

target.write("M")
target.write(",")
target.write(str(m[0]))
target.write(",")
target.write(str(m[1]))
target.write(",")
target.write(str(m[2]))
target.write(",")
target.write(str(m[3]))
target.write(",")
target.write(str(m[4]))
target.write(",")
target.write(str(m[5]))
target.write(",")
target.write(str(m[6]))
target.write(",")
target.write(str(m[7]))
target.write(",")
target.write(str(m[8]))
target.write(",")
target.write(str(m[9]))
target.write(",")
target.write(str(m[10]))
target.write(",")
target.write(str(m[11]))
target.write(",")
target.write(str(m[12]))
target.write(",")
target.write(str(m[13]))
target.write(",")
target.write(str(m[14]))
target.write(",")
target.write(str(m[15]))
target.write('\n')

target.write("C")
target.write(",")
target.write(str(c[0]))
target.write(",")
target.write(str(c[1]))
target.write(",")
target.write(str(c[2]))
target.write(",")
target.write(str(c[3]))
target.write(",")
target.write(str(c[4]))
target.write(",")
target.write(str(c[5]))
target.write(",")
target.write(str(c[6]))
target.write(",")
target.write(str(c[7]))
target.write(",")
target.write(str(c[8]))
target.write(",")
target.write(str(c[9]))
target.write(",")
target.write(str(c[10]))
target.write(",")
target.write(str(c[11]))
target.write(",")
target.write(str(c[12]))
target.write(",")
target.write(str(c[13]))
target.write(",")
target.write(str(c[14]))
target.write(",")
target.write(str(c[15]))
target.write('\n')

target.write("VM")
target.write(",")
target.write(str(vm))
target.write('\n')

target.write("VC")
target.write(",")
target.write(str(vc))
target.write('\n')

target.write('\n')
