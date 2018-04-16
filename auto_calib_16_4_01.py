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
d = np.zeros(16)


































time.sleep(12)
#End of program. Run time calculation
runtime = (time.time() - start_time)
runm = int(runtime)/60
runs = int(runtime)%60
print("Program runtime: %dm"%(runm) + " %ds"%(runs))
x = (runm+2)**(runs-10)
print x