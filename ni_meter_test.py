import minimalmodbus
import serial
import time
import numpy as np
import statistics
import nidaqmx
import nidaqmx.system

system = nidaqmx.system.System.local()
system.driver_version
DriverVersion(major_version=16L, minor_version=0L, update_version=0L)
for device in system.devices:
 print(device)

#Define Communication parameters
minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1
#not closing port after each call causes buffer overflow issue(Probably?)
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

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

x[0][0] = smb.read_registers(3,8,3)
y[0][0] = meter.read_registers(3,8,3)

with nidaqmx.Task() as task:
 task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
 ref = task.read()
 print(ref) 

 
 
