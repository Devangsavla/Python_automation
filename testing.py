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

# Input Slave ID in normal decimal
db = input('Enter Daughter Board Number: ')
mb = input('Enter Mother Board Number: ')
b  = input('Enter Slave ID: ')
time.sleep(1)

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

#Define PCB Com port
smb = minimalmodbus.Instrument('COM3',b,mode='rtu')
smb.debug= False

raw_input("Set Voltage to 500V and PRESS ENTER")
vy[0] = raw_input("Enter voltage source value and press ENTER: ")
print("Multimeter voltage 1: "),vy[0]
try:
 vx[0] = smb.read_register(25,1,4)
except IOError:
 print("Failed to read from instrument")
print("PCB voltage 1: "),vx[0]


raw_input("Set Voltage to 1000V and PRESS ENTER")
vy[1] = raw_input("Enter Fluke voltage value and press ENTER: ")
print("Multimeter voltage 2: "),vy[1]
vx[1]= smb.read_register(25,1,4)
print("PCB voltage 2: "),vx[1]

raw_input("Set Voltage to 1500V and PRESS ENTER")
vy[2] = raw_input("Enter Fluke voltage value and press ENTER: ")
print("Multimeter voltage 3: "),vy[2]
vx[2]= smb.read_register(25,1,4)
print("PCB voltage 3: "),vx[2]