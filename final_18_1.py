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

#Define Fluke meter parameters
# ser1 = serial.Serial(
	# port = 'COM3',
	# baudrate = 115200,
    # parity = serial.PARITY_NONE,
    # stopbits = serial.STOPBITS_ONE,
    # bytesize = serial.EIGHTBITS,
    # timeout = 1
	# )
# init1='\x51\x4D\x0D'

#function to check if slave ID entered is valid or not
def slave_id(a):
 id = input('Enter Slave ID of board %d: ' %a)
 if id not in range(1,200):
  print("Invalid Input. Try again: ")
  slave_id(a)
 return id
 
#function whose input is x & y lists and output is m & c lists
def regression(x_s,y_s):
 # mean of all elements
 # dividing by 10 to avoid overflow in calculation
 x_mean= 0.1*statistics.mean(x_s)
 y_mean= 0.1*statistics.mean(y_s)

 # square every element
 x2=0.1*0.1*x_s*x_s
 x2_mean = statistics.mean(x2)

 # element wise multiplication of 2 list
 xy=0.1*0.1*x_s*y_s
 xy_mean = statistics.mean(xy)

 # regression calculation
 # not multiplying 10 back as it gets canceled in Nr and Dr
 m = ((x_mean * y_mean) - xy_mean)/((x_mean*x_mean) - x2_mean)
 m=round(m,4)
 # multiplying back by 10
 c = 10*round(y_mean - (x_mean*m))
 return m,c
 
#function to read 8 channel voltage from NI card
def nidata():
 for i in range(0,8):
  ch = 'Dev1/ai' + str(i)
  with nidaqmx.Task() as task:
   task.ai_channels.add_ai_voltage_chan(ch, max_val=0.04, min_val=0)
   time.sleep(0.1)
   ym[i] = 100000*task.read()
   ym[i] = ym[i]+ 100000*task.read()
   ym[i] = ym[i]+ 100000*task.read()
   ym[i] = ym[i]+ 100000*task.read()
   ym[i] = ym[i]+ 100000*task.read()
   ym[i] = ym[i]+ 100000*task.read()
   ym[i] = ym[i]+ 100000*task.read()
   ym[i] = ym[i]+ 100000*task.read()
   ym[i] = ym[i]+ 100000*task.read()
   ym[i] = ym[i]+ 100000*task.read()
   time.sleep(0.5)
 return(ym)

# def vread():
 # ser1.write(init1)
 # time.sleep(1)
 # while ser1.inWaiting():
  # time.sleep(1)
  # read_data1 = ser1.readline()
  # list1 = read_data1.split('\x2C')
  # list4 = list1[0].split('\r')
  # return list4[1]
 
# Input Slave ID in normal decimal
sn = raw_input("Enter PCB Serial Number: ")
b=slave_id(1)
print("Serial Number: "),sn
print("Slave ID: "),b
time.sleep(1)

#Define PCB Com port
smb = minimalmodbus.Instrument('COM15',b,mode='rtu')
smb.debug= False

#Define Fluke Multimeter Com Port
# ser1 = serial.Serial(
	# port = 'COM3',
	# baudrate = 115200,
    # parity = serial.PARITY_NONE,
    # stopbits = serial.STOPBITS_ONE,
    # bytesize = serial.EIGHTBITS,
    # timeout = 1
	# )

# create 3D list for 2 settings 3 current and 8 channels
x = np.zeros((2,3,8))
y = np.zeros((2,3,8))
# create master 2D list for 3 current and 16 channels
chx = np.zeros((16,3))
chy = np.zeros((16,3))
# create m and c lists for all 16 channels
m = np.zeros(16)
c = np.zeros(16)
ym = np.zeros(8)
vx = np.zeros(3)
vy = np.zeros(3)
vx1=0
vy1=0
vx2=0
vy2=0
vx3=0
vy3=0

# Read all raw data of all 16 channels at 3 different current settings
chk='n'
while(chk=='n'):
 raw_input("Keep setting A and current 3A and PRESS ENTER")
 time.sleep(5)
 x[0][0] = smb.read_registers(1,8,4)
 print(x[0][0])
 y[0][0]=nidata()
 print(y[0][0])
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(3)

chk='n'
while(chk=='n'):
 raw_input("Keep setting B and current 3A and PRESS ENTER")
 time.sleep(5)
 x[1][0]= smb.read_registers(9,8,4)
 print(x[1][0])
 y[1][0]=nidata()
 print(y[1][0])
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(3)

chk='n'
while(chk=='n'):
 raw_input("Keep setting B and current 15A and PRESS ENTER")
 time.sleep(5)
 x[1][1]= smb.read_registers(9,8,4)
 print(x[1][1])
 y[1][1]=nidata()
 print(y[1][1])
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(3)

chk='n'
while(chk=='n'):
 raw_input("Keep setting A and current 15A and PRESS ENTER")
 time.sleep(5)
 x[0][1]= smb.read_registers(1,8,4)
 print(x[0][1])
 y[0][1]=nidata()
 print(y[0][1])
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(3)

chk='n'
while(chk=='n'):
 raw_input("Keep setting A and current 30A and PRESS ENTER")
 time.sleep(5)
 x[0][2]= smb.read_registers(1,8,4)
 print(x[0][2])
 y[0][2]=nidata()
 print(y[0][2])
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(3)
 
chk='n'
while(chk=='n'):
 raw_input("Keep setting B and current 30A and PRESS ENTER")
 time.sleep(5)
 x[1][2]= smb.read_registers(9,8,4)
 print(x[1][2])
 y[1][2]=nidata()
 print(y[1][2])
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(3)

#Rearrange x and y data as per channel
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
m = 10000*m
print("m"),m
print("c"),c

raw_input("If constants are fine press PRESS ENTER")

raw_input("Set Voltage to 300V and PRESS ENTER")
vx1= smb.read_registers(25,1,4)
print("PCB voltage 1: "),vx1
vy1 = raw_input("Enter Fluke voltage value and press ENTER: ")
print("Multimeter voltage 1: "),vy1

raw_input("Set Voltage to 500V and PRESS ENTER")
vx2= smb.read_registers(25,1,4)
print("PCB voltage 2: "),vx2
vy2 = raw_input("Enter Fluke voltage value and press ENTER: ")
print("Multimeter voltage 2: "),vy2

raw_input("Set Voltage to 900V and PRESS ENTER")
vx3= smb.read_registers(25,1,4)
print("PCB voltage 3: "),vx3
vy3 = raw_input("Enter Fluke voltage value and press ENTER: ")
print("Multimeter voltage 3: "),vy3

vm = raw_input("Enter Voltage M: ")
print("voltage m: "),vm
vc = raw_input("Enter Voltage C: ")
print("voltage c: "),vc

raw_input("All OK to write then PRESS ENTER")
smb.write_registers(0,[int(m[0]),int(m[1]),int(m[2]),int(m[3]),int(m[4]),int(m[5]),int(m[6]),int(m[7]),int(m[8]),int(m[9]),int(m[10]),int(m[11]),int(m[12]),int(m[13]),int(m[14]),int(m[15]),abs(int(c[0])),abs(int(c[1])),abs(int(c[2])),abs(int(c[3])),abs(int(c[4])),abs(int(c[5])),abs(int(c[6])),abs(int(c[7])),abs(int(c[8])),abs(int(c[9])),abs(int(c[10])),abs(int(c[11])),abs(int(c[12])),abs(int(c[13])),abs(int(c[14])),abs(int(c[15])),int(vm),int(vc)])

# vx[0]=vx1
# vy[0]=vy1
# vx[1]=vx2
# vy[1]=vy2
# vx[2]=vx3
# vy[2]=vy3

# print("PCB voltage: ",vx)
# print("Multimeter voltage: ",vy)

# vm,vc = regression(vx,vy)
# print("Voltage m: "),vm
# print("Voltage c: "),vc

# target = open("log_calib.csv","a")

# target.write("Serial number")
# target.write(",")
# target.write(str(sn))
# target.write('\n')

# target.write("Slave ID")
# target.write(",")
# target.write(str(b))
# target.write('\n')

# target.write(str(1))
# target.write(",")
# target.write(str(2)x`)
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
# target.write(",")
# target.write(str(c[16]))
# target.write('\n')

# target.write("Voltage M")
# target.write(",")
# target.write(str(vm))
# target.write('\n')
# target.write("Voltage C")
# target.write(",")
# target.write(str(vc))
# target.write('\n')

# target.write('\n')
# target.close()