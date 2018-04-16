import minimalmodbus
import serial
import time
import numpy as np
import statistics
import nidaqmx

#Define Communication parameters
minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1
#not closing port after each call causes buffer overflow issue(Probably?)
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

# db = input('Enter Daughter Board Number: ')
# mb = input('Enter Mother Board Number: ')
# s = input('Enter Slave ID: ')

smb = minimalmodbus.Instrument('COM15',3,mode='rtu')
smb.debug= False

# target = open("log_calib.csv","a")

m = np.zeros(16)
c = np.zeros(16)
d = np.zeros(16)

raw_input("PRESS ENTER to read Slope M: ")
time.sleep(2)
m = smb.read_registers(0,16,3)
print("M: "),m

raw_input("PRESS ENTER to read Constant C: ")
time.sleep(2)
c = smb.read_registers(16,16,3)
print("C: "),c

print("new = old - difference")

d[0]= 40
d[1]= 40
d[2]= 40
d[3]= 40
d[4]= 40
d[5]= 40
d[6]= 40
d[7]= 40
d[8]= 40
d[9]= 40
d[10]= 40
d[11]= 40
d[12]= 40
d[13]= 40
d[14]= 40
d[15]= 40

c[0] =  int(c[0] - d[0])       #Channel 1
c[1] =  int(c[1] - d[1])       #Channel 2
c[2] =  int(c[2] - d[2])       #Channel 3
c[3] =  int(c[3] - d[3])       #Channel 4
c[4] =  int(c[4] - d[4])       #Channel 5
c[5] =  int(c[5] - d[5])       #Channel 6  
c[6] =  int(c[6] - d[6])       #Channel a 
c[7] =  int(c[7] - d[7])       #Channel b
c[8] =  int(c[8] - d[8])       #Channel 7
c[9] =  int(c[9] - d[9])       #Channel 8
c[10] = int(c[10]- d[10])      #Channel 9
c[11] = int(c[11]- d[11])      #Channel 10
c[12] = int(c[12]- d[12])      #Channel 11
c[13] = int(c[13]- d[13])      #Channel 12
c[14] = int(c[14]- d[14])      #Channel c
c[15] = int(c[15]- d[15])      #Channel d

print("Modified C: "),c

vm=9140
vc=2

raw_input("If all constants are OK, Change program and PRESS ENTER.")

raw_input("All OK to write then PRESS ENTER")
smb.write_registers(0,[m[0],m[1],m[2],m[3],m[4],m[5],m[6],m[7],m[8],m[9],m[10],m[11],m[12],m[13],m[14],m[15],c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[12],c[13],c[14],c[15],vm,vc])

raw_input("Change Complete. Press Enter to record in Excel")
time.sleep(1)

# target.write('\n')
# target.write("Daughter Board ID")
# target.write(",")
# target.write("Mother Board ID")
# target.write(",")
# target.write("Slave ID")
# target.write('\n')

# target.write(str(db))
# target.write(",")
# target.write(str(mb))
# target.write(",")
# target.write(str(s))
# target.write('\n')

# target.write("Channel Number")
# target.write(",")
# target.write(str(1))
# target.write(",")
# target.write(str(2))
# target.write(",")
# target.write(str(3))
# target.write(",")
# target.write(str(4))
# target.write(",")
# target.write(str(5))
# target.write(",")
# target.write(str(6))
# target.write(",")
# target.write(str(7))
# target.write(",")
# target.write(str(8))
# target.write(",")
# target.write(str(9))
# target.write(",")
# target.write(str(10))
# target.write(",")
# target.write(str(11))
# target.write(",")
# target.write(str(12))
# target.write(",")
# target.write(str(13))
# target.write(",")
# target.write(str(14))
# target.write(",")
# target.write(str(15))
# target.write(",")
# target.write(str(16))
# target.write('\n')

# target.write("M")
# target.write(",")
# target.write(str(m[0]))
# target.write(",")
# target.write(str(m[1]))
# target.write(",")
# target.write(str(m[2]))
# target.write(",")
# target.write(str(m[3]))
# target.write(",")
# target.write(str(m[4]))
# target.write(",")
# target.write(str(m[5]))
# target.write(",")
# target.write(str(m[6]))
# target.write(",")
# target.write(str(m[7]))
# target.write(",")
# target.write(str(m[8]))
# target.write(",")
# target.write(str(m[9]))
# target.write(",")
# target.write(str(m[10]))
# target.write(",")
# target.write(str(m[11]))
# target.write(",")
# target.write(str(m[12]))
# target.write(",")
# target.write(str(m[13]))
# target.write(",")
# target.write(str(m[14]))
# target.write(",")
# target.write(str(m[15]))
# target.write('\n')

# target.write("C")
# target.write(",")
# target.write(str(c[0]))
# target.write(",")
# target.write(str(c[1]))
# target.write(",")
# target.write(str(c[2]))
# target.write(",")
# target.write(str(c[3]))
# target.write(",")
# target.write(str(c[4]))
# target.write(",")
# target.write(str(c[5]))
# target.write(",")
# target.write(str(c[6]))
# target.write(",")
# target.write(str(c[7]))
# target.write(",")
# target.write(str(c[8]))
# target.write(",")
# target.write(str(c[9]))
# target.write(",")
# target.write(str(c[10]))
# target.write(",")
# target.write(str(c[11]))
# target.write(",")
# target.write(str(c[12]))
# target.write(",")
# target.write(str(c[13]))
# target.write(",")
# target.write(str(c[14]))
# target.write(",")
# target.write(str(c[15]))
# target.write('\n')

# target.write("VM")
# target.write(",")
# target.write(str(vm))
# target.write('\n')

# target.write("VC")
# target.write(",")
# target.write(str(vc))
# target.write('\n')

# target.write('\n')
