import minimalmodbus
import serial
import time
import numpy as np
import statistics
import nidaqmx

vx = np.zeros(3)
vy = np.zeros(3)

ser1 = serial.Serial(
	port = 'COM3',
	baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
	)
init1='\x51\x4D\x0D'

#Define PCB Com port
smb = minimalmodbus.Instrument('COM15',3,mode='rtu')
smb.debug= False

#Define Communication parameters
minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1
#not closing port after each call causes buffer overflow issue(Probably?)
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

raw_input("Set Voltage to 300V and PRESS ENTER")
vx[0]= smb.read_registers(25,1,4)
print("PCB voltage 1: ",vx[0])
vy[0] = vread()
print("Multimeter voltage 1: ",vy[0])

raw_input("Set Voltage to 500V and PRESS ENTER")
vx[1]= smb.read_registers(25,1,4)
print("PCB voltage 2: ",vx[1])
vy[1] = vread()
print("Multimeter voltage 2: ",vy[1])

raw_input("Set Voltage to 900V and PRESS ENTER")
vx[2]= smb.read_registers(25,1,4)
print("PCB voltage 3: ",vx[2])
vy[2] = vread()
print("Multimeter voltage 3: ",vy[2])

print("Multimeter voltage: ",vx)

def vread():
 ser1.write(init1)
 time.sleep(1)
 while ser1.inWaiting():
  time.sleep(1)
  read_data1 = ser1.readline()
  list1 = read_data1.split('\x2C')
  list4 = list1[0].split('\r')
  return list4[1]