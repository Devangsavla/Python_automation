import minimalmodbus
import serial
import time
import numpy as np

#Define Communication parameters
minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1
#not closing port after each call causes buffer overflow issue(Probably?)
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

#Define PCB Com port
smb = minimalmodbus.Instrument('COM4',1,mode='rtu')
smb.debug= False

while(1):
 for i in range(1,8):
  x = pow(2,i)
  print x
  smb.write_register(64,x)

# while(1):
 # smb.write_register(64,1)
 # #time.sleep(0.1)
 # smb.write_register(64,3)
 # #time.sleep(0.1)
 # smb.write_register(64,7)
 # #time.sleep(0.1)
 # smb.write_register(64,15)
 # #time.sleep(0.1)
 # smb.write_register(64,31)
 # #time.sleep(0.1)
 # smb.write_register(64,63)
 # #time.sleep(0.1)
 # smb.write_register(64,127)
 # #time.sleep(0.1)
 # smb.write_register(64,255)
 # #time.sleep(0.1)
 
