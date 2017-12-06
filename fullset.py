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

x11smb, x12smb, x13smb, x21smb, x22smb, x23smb, y11smb, y12smb, y13smb, y21smb, y22smb, y23smb = ([] for i in range(12))

def slave_id(a):
 x = input('Enter Slave ID of board %d: ' %a)
 if x not in range(1,20):
  print("Invalid Input. Try again: ")
  slave_id(a)
 return x

def modread(s,c):
 if s==1:
  if c==1:
   time.sleep(1)
   x11smb  = x11smb + smb.read_registers(3,8,3)
   y11smb  = y11smb + meter.read_registers(3,8,3)
   print('x11smb: '),x11smb
   print('y11smb: '),y11smb
  if c==2:
   time.sleep(1)
   x12smb  = x12smb + smb.read_registers(3,8,3)
   y12smb  = y12smb + meter.read_registers(3,8,3)
   print('x12smb: '),x12smb
   print('y12smb: '),y12smb
  if c==3:
   time.sleep(1)
   x13smb  = x13smb + smb.read_registers(3,8,3)
   y13smb  = y13smb + meter.read_registers(3,8,3)
   print('x13smb: '),x13smb
   print('y13smb: '),y13smb
 if s==2:
  if c==1:
   time.sleep(1)
   x21smb  = x21smb + smb.read_registers(11,8,3)
   y21smb  = y21smb + meter.read_registers(3,8,3)
   print('x21smb: '),x21smb
   print('y21smb: '),y21smb
  if c==2:
   time.sleep(1)
   x22smb  = x22smb + smb.read_registers(11,8,3)
   y22smb  = y22smb + meter.read_registers(3,8,3)
   print('x22smb: '),x22smb
   print('y22smb: '),y22smb
  if c==3:
   time.sleep(1)
   x23smb  = x23smb + smb.read_registers(11,8,3)
   y23smb  = y23smb + meter.read_registers(3,8,3)
   print('x23smb: '),x23smb
   print('y23smb: '),y23smb
 
b=slave_id(1)
print ("Board IDs: "),b
time.sleep(1)

smb = minimalmodbus.Instrument('COM15',b,mode='rtu')
smb.debug= False
meter = minimalmodbus.Instrument('COM16',3,mode='rtu')
meter.debug= False

raw_input("Keep setting A and current 3A and PRESS ENTER")
modread(1,1)
time.sleep(1)

raw_input("Keep setting B and current 3A and PRESS ENTER")
modread(2,1)
time.sleep(1)

raw_input("Keep setting B and current 15A and PRESS ENTER")
modread(2,2)
time.sleep(1)

raw_input("Keep setting A and current 15A and PRESS ENTER")
modread(1,2)
time.sleep(1)

raw_input("Keep setting A and current 30A and PRESS ENTER")
modread(1,3)
time.sleep(1)

raw_input("Keep setting B and current 30A and PRESS ENTER")
modread(2,3)
time.sleep(1)