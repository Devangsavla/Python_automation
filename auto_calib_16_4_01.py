import minimalmodbus
import serial
import numpy as np
import datetime
import time

dt = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
print "Present Date and Time: " ,dt
start_time = time.time()

#Define Modbus Parameters
minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1
#not closing port after each call causes buffer overflow issue(Probably?)
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

#Define Fluke Serial Parameters
ser1 = serial.Serial(
 port = 'COM2',
 baudrate = 115200,
 parity = serial.PARITY_NONE,
 stopbits = serial.STOPBITS_ONE,
 bytesize = serial.EIGHTBITS,
 timeout = 1
 )

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

def fluke():
 init1='\x51\x4D\x0D'
 while 1:
  ser1.write(init1)
  time.sleep(0.1)
  while ser1.inWaiting():
   #time.sleep(5)
   read_data1 = ser1.readline()
   list1 = read_data1.split('\x2C')
   f = list1[0].split('\r')
   print(list4[1])
  return f
 
# Input Slave ID in normal decimal
db = input('Enter Daughter Board Number: ')
mb = input('Enter Mother Board Number: ')
b  = input('Enter Slave ID: ')
time.sleep(1)

#Define PCB Com port
smb = minimalmodbus.Instrument('COM3',b,mode='rtu')
smb.debug= False

#Define IO Card Current Com port
io1 = minimalmodbus.Instrument('COM3',1,mode='rtu')
io1.debug= False

#Define IO Card Channel Com port
io2 = minimalmodbus.Instrument('COM3',2,mode='rtu')
io2.debug= False

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
d = np.zeros(16)

raw_input("Keep setting A and press enter>")
for i in range(0,4):
 cu = 2**i
 #Current 1 to 4
 # smb.write_register(64,cu)
 print("Set Current: %d" %(i+1))
 for j in range(0,8):
  ch = 2**j
  print("Reading Channel: %d" %(j+1))
  #Channel 1 to 8
  smb.write_register(64,ch)
  x_temp = smb.read_register(ch,4)
  y_temp = fluke() 
  x[0][cu-1][ch-1] = x_temp
  y[0][cu-1][ch-1] = y_temp
  
raw_input("Keep setting B and press enter>")
for i in range(0,4):
 cu = 2**i
 #Current 1 to 4
 # smb.write_register(64,cu)
 print("Set Current: %d" %(i+1))
 for j in range(0,8):
  ch = 2**j
  print("Reading Channel: %d" %(j+1))
  #Channel 1 to 8
  smb.write_register(64,ch)
  x_temp = smb.read_register(ch,4)
  y_temp = fluke() 
  x[1][cu-1][ch-1] = x_temp
  y[1][cu-1][ch-1] = y_temp
  
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
print("m"),m
print("c"),c

raw_input("Set Voltage to 500V and PRESS ENTER")
vy[0] = fluke()
print("Multimeter voltage 1: "),vy[0]
vx[0] = smb.read_register(25,4)
print("PCB voltage 1: "),vx[0]


raw_input("Set Voltage to 1000V and PRESS ENTER")
vy[1] = fluke()
print("Multimeter voltage 2: "),vy[1]
vx[1] = smb.read_register(25,4)
print("PCB voltage 2: "),vx[1]

raw_input("Set Voltage to 1500V and PRESS ENTER")
vy[2] = fluke()
print("Multimeter voltage 3: "),vy[2]
vx[2] = smb.read_register(25,4)
print("PCB voltage 3: "),vx[2]

vm,vc = regression(vx,vy)
vm = int(vm*10000)
vc = int(vc)
print("Raw Vc: "),vc
if vc < 0:
 vc = 0

print("VM: "),int(vm)
print("VC: "),int(vc)

raw_input("All OK to write then PRESS ENTER")
smb.write_registers(0,[int(m[0]),int(m[1]),int(m[2]),int(m[3]),int(m[4]),int(m[5]),int(m[6]),int(m[7]),int(m[8]),int(m[9]),int(m[10]),int(m[11]),int(m[12]),int(m[13]),int(m[14]),int(m[15]),abs(int(c[0])),abs(int(c[1])),abs(int(c[2])),abs(int(c[3])),abs(int(c[4])),abs(int(c[5])),abs(int(c[6])),abs(int(c[7])),abs(int(c[8])),abs(int(c[9])),abs(int(c[10])),abs(int(c[11])),abs(int(c[12])),abs(int(c[13])),abs(int(c[14])),abs(int(c[15])),int(vm),int(vc)])
time.sleep(2)



































#End of program. Run time calculation
runtime = (time.time() - start_time)
runm = int(runtime)/60
runs = int(runtime)%60
print("Program runtime: %dm"%(runm) + " %ds"%(runs))