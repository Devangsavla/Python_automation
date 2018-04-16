import serial,time
from datetime import datetime
from time import sleep
# 1 is for data from DMM (Fluke287)
ser1 = serial.Serial(
 port = 'COM2',
 baudrate = 115200,
 parity = serial.PARITY_NONE,
 stopbits = serial.STOPBITS_ONE,
 bytesize = serial.EIGHTBITS,
 timeout = 1
 )
	
#print('starting communication')
init1='\x51\x4D\x0D'
while 1:
 ser1.write(init1)
 time.sleep(0.1)
 while ser1.inWaiting():
  #time.sleep(5)
  read_data1 = ser1.readline()
  list1 = read_data1.split('\x2C')
  list4 = list1[0].split('\r')
  print(list4[1])