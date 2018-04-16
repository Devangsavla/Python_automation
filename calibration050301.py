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
 c = 10*(y_mean - (x_mean*m))
 c = round(c)
 # c = c-20
 return m,c
 
#function to read 8 channel voltage from NI card
def nidata():
 for i in range(0,8):
  ch = 'Dev1/ai' + str(i)
  with nidaqmx.Task() as task:
   task.ai_channels.add_ai_voltage_chan(ch, max_val=0.04, min_val=0)
   time.sleep(0.1)
   ym[i] = 100000*task.read()
   time.sleep(0.1)
   ym[i] = ym[i]+ 100000*task.read()
   time.sleep(0.1)
   ym[i] = ym[i]+ 100000*task.read()
   time.sleep(0.1)
   ym[i] = ym[i]+ 100000*task.read()
   time.sleep(0.1)
   ym[i] = ym[i]+ 100000*task.read()
   time.sleep(0.1)
   ym[i] = ym[i]+ 100000*task.read()
   time.sleep(0.1)
   ym[i] = ym[i]+ 100000*task.read()
   time.sleep(0.1)
   ym[i] = ym[i]+ 100000*task.read()
   time.sleep(0.1)
   ym[i] = ym[i]+ 100000*task.read()
   time.sleep(0.1)
   ym[i] = ym[i]+ 100000*task.read()
   # ym[i] = ym[i]+ 100
   ym[i] = round(ym[i])
 return(ym)
 
# Input Slave ID in normal decimal
db = input('Enter Daughter Board Number: ')
mb = input('Enter Mother Board Number: ')
b  = input('Enter Slave ID: ')
time.sleep(1)

#Define PCB Com port
smb = minimalmodbus.Instrument('COM3',b,mode='rtu')
smb.debug= False

# create 3D list for 2 settings 5 current and 8 channels
x = np.zeros((2,5,8))
y = np.zeros((2,5,8))
diff = np.zeros(8)
# create master 2D list for 5 current and 16 channels
chx = np.zeros((16,5))
chy = np.zeros((16,5))
# create m and c lists for all 16 channels
m = np.zeros(16)
c = np.zeros(16)
ym = np.zeros(8)
vx = np.zeros(3)
vy = np.zeros(3)

# Read all raw data of all 16 channels at 3 different current settings
#3A
chk='n'
while(chk=='n'):
 raw_input("Keep setting A and current 3A and PRESS ENTER")
 print("Wait for Reading...")
 time.sleep(15)
 try:
  x[0][0] = smb.read_registers(1,8,4)
 except IOError:
  print("Failed to read from instrument")
 print(x[0][0])
 y[0][0]=nidata()
 print(y[0][0])
 for i in range (0,8):
  diff[i] = x[0][0][i] - y[0][0][i]
 print("Difference: ")
 print(diff)
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(1)

#3B
chk='n'
while(chk=='n'):
 raw_input("Keep setting B and current 3A and PRESS ENTER")
 print("Wait for Reading...")
 time.sleep(15)
 x[1][0]= smb.read_registers(9,8,4)
 print(x[1][0])
 y[1][0]=nidata()
 print(y[1][0])
 for i in range (0,8):
  diff[i] = x[1][0][i] - y[1][0][i]
 print("Difference: ")
 print(diff)
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(1)

#5B
chk='n'
while(chk=='n'):
 raw_input("Keep setting B and current 5A and PRESS ENTER")
 print("Wait for Reading...")
 time.sleep(15)
 x[1][1]= smb.read_registers(9,8,4)
 print(x[1][1])
 y[1][1]=nidata()
 print(y[1][1])
 for i in range (0,8):
  diff[i] = x[1][1][i] - y[1][1][i]
 print("Difference: ")
 print(diff)
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(1)

#5A
chk='n'
while(chk=='n'):
 raw_input("Keep setting A and current 5A and PRESS ENTER")
 print("Wait for Reading...")
 time.sleep(15)
 x[0][1]= smb.read_registers(1,8,4)
 print(x[0][1])
 y[0][1]=nidata()
 print(y[0][1])
 for i in range (0,8):
  diff[i] = x[0][1][i] - y[0][1][i]
 print("Difference: ")
 print(diff)
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(1)

#10A
chk='n'
while(chk=='n'):
 raw_input("Keep setting A and current 10A and PRESS ENTER")
 print("Wait for Reading...")
 time.sleep(15)
 x[0][2]= smb.read_registers(1,8,4)
 print(x[0][2])
 y[0][2]=nidata()
 print(y[0][2])
 for i in range (0,8):
  diff[i] = x[0][2][i] - y[0][2][i]
 print("Difference: ")
 print(diff)
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(1)

#10B
chk='n'
while(chk=='n'):
 raw_input("Keep setting B and current 10A and PRESS ENTER")
 print("Wait for Reading...")
 time.sleep(15)
 x[1][2]= smb.read_registers(9,8,4)
 print(x[1][2])
 y[1][2]=nidata()
 print(y[1][2])
 for i in range (0,8):
  diff[i] = x[1][2][i] - y[1][2][i]
 print("Difference: ")
 print(diff)
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(1)

#15B
chk='n'
while(chk=='n'):
 raw_input("Keep setting B and current 15A and PRESS ENTER")
 print("Wait for Reading...")
 time.sleep(15)
 x[1][3]= smb.read_registers(9,8,4)
 print(x[1][3])
 y[1][3]=nidata()
 print(y[1][3])
 for i in range (0,8):
  diff[i] = x[1][3][i] - y[1][3][i]
 print("Difference: ")
 print(diff)
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(1)

#15A
chk='n'
while(chk=='n'):
 raw_input("Keep setting A and current 15A and PRESS ENTER")
 print("Wait for Reading...")
 time.sleep(15)
 x[0][3]= smb.read_registers(1,8,4)
 print(x[0][3])
 y[0][3]=nidata()
 print(y[0][3])
 for i in range (0,8):
  diff[i] = x[0][3][i] - y[0][3][i]
 print("Difference: ")
 print(diff)
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(1)
 
#20A
chk='n'
while(chk=='n'):
 raw_input("Keep setting A and current 20A and PRESS ENTER")
 print("Wait for Reading...")
 time.sleep(15)
 x[0][4]= smb.read_registers(1,8,4)
 print(x[0][4])
 y[0][4]=nidata()
 print(y[0][4])
 for i in range (0,8):
  diff[i] = x[0][4][i] - y[0][4][i]
 print("Difference: ")
 print(diff)
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(1)
 
#20B
chk='n'
while(chk=='n'):
 raw_input("Keep setting B and current 20A and PRESS ENTER")
 print("Wait for Reading...")
 time.sleep(15)
 x[1][4]= smb.read_registers(9,8,4)
 print(x[1][4])
 y[1][4]=nidata()
 print(y[1][4])
 for i in range (0,8):
  diff[i] = x[1][4][i] - y[1][4][i]
 print("Difference: ")
 print(diff)
 chk = raw_input(" If data is correct press ENTER. If data is incorrect press n and then PRESS ENTER.")
 time.sleep(1)

#Rearrange x and y data as per channel
for i in range(0,8):
 chx[i] = x[0][0][i] , x[0][1][i] , x[0][2][i], x[0][3][i], x[0][4][i]
 print(" Chx %d"%(i+1)),chx[i]
 chy[i] = y[0][0][i] , y[0][1][i] , y[0][2][i], y[0][3][i], y[0][4][i]
 print(" Chy %d"%(i+1)),chy[i]
for i in range(0,8):
 chx[i+8] = x[1][0][i] , x[1][1][i] , x[1][2][i], x[1][3][i], x[1][4][i]
 print(" Chx %d"%(i+9)),chx[i]
 chy[i+8] = y[1][0][i] , y[1][1][i] , y[1][2][i], y[1][3][i], y[1][4][i]
 print(" Chy %d"%(i+9)),chy[i]
print("Input Done!")

#Regression
for i in range(0,16):
 m[i],c[i] = regression(chx[i],chy[i])
print("Current Done!")
m = 10000*m

raw_input("Set Voltage to 500V and PRESS ENTER")
vy[0] = raw_input("Enter voltage source value and press ENTER: ")
print("Multimeter voltage 1: "),vy[0]
try:
 x[0][0] = smb.read_registers(1,8,4)
except IOError:
 print("Failed to read from instrument")

vx[0]= smb.read_registers(25,1,4)
print("PCB voltage 1: "),vx[0]


raw_input("Set Voltage to 1000V and PRESS ENTER")
vy[1] = raw_input("Enter Fluke voltage value and press ENTER: ")
print("Multimeter voltage 2: "),vy[1]
vx[1]= smb.read_registers(25,1,4)
print("PCB voltage 2: "),vx[1]

raw_input("Set Voltage to 1500V and PRESS ENTER")
vy[2] = raw_input("Enter Fluke voltage value and press ENTER: ")
print("Multimeter voltage 3: "),vy[2]
vx[2]= smb.read_registers(25,1,4)
print("PCB voltage 3: "),vx[2]

vm,vc = regression(vx,vy)
vm = int(vm*10000)
vc = int(vc)
# vm=9140
# vc=2

print("m"),m
print("c"),c
print("VM: "),int(vm)
print("VC: "),int(vc)

raw_input("All OK to write then PRESS ENTER")
smb.write_registers(0,[int(m[0]),int(m[1]),int(m[2]),int(m[3]),int(m[4]),int(m[5]),int(m[6]),int(m[7]),int(m[8]),int(m[9]),int(m[10]),int(m[11]),int(m[12]),int(m[13]),int(m[14]),int(m[15]),abs(int(c[0])),abs(int(c[1])),abs(int(c[2])),abs(int(c[3])),abs(int(c[4])),abs(int(c[5])),abs(int(c[6])),abs(int(c[7])),abs(int(c[8])),abs(int(c[9])),abs(int(c[10])),abs(int(c[11])),abs(int(c[12])),abs(int(c[13])),abs(int(c[14])),abs(int(c[15])),int(vm),int(vc)])
time.sleep(2)

print("Daughter Board Serial Number: "),sn
print("Daughter Board Serial Number: "),sn
print("Slave ID: "),b

raw_input("PRESS ENTER to read >")
time.sleep(1)

m = smb.read_registers(0,16,3)
print("M: "),m
c = smb.read_registers(16,16,3)
print("C: "),c

raw_input("Keep Setting A and current 3A and PRESS ENTER")
time.sleep(15)
for i in range(0,8):
 y[i] = raw_input("Enter multimeter value for Channel %d : "%(i+1))
 x[i] = smb.read_registers((i+1),1,4)
 d[i] = 10*round((y[i]-x[i])/10)
 c[i] = int(c[i]-d[i])

raw_input("Keep Setting B and current 3A and PRESS ENTER")
time.sleep(15)
for i in range(8,8):
 y[i] = raw_input("Enter multimeter value for Channel %d : "%(i+1))
 x[i] = smb.read_registers((i+1),1,4)
 d[i] = 10*round((y[i]-x[i])/10)
 c[i] = int(c[i]-d[i])

print("Difference list: "),d
print("C after difference: "),c	

vm=smb.read_registers(32,1,4)
vc=smb.read_registers(33,1,4)

print("VM: "),int(vm)
print("VC: "),int(vc)

raw_input("All OK to write then PRESS ENTER")
smb.write_registers(0,[m[0],m[1],m[2],m[3],m[4],m[5],m[6],m[7],m[8],m[9],m[10],m[11],m[12],m[13],m[14],m[15],c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8],c[9],c[10],c[11],c[12],c[13],c[14],c[15],vm,vc])

c = smb.read_registers(16,16,3)
print("Modified C: "),c

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
