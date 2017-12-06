import minimalmodbus
import serial
from time import sleep

minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1

instrument = minimalmodbus.Instrument('COM15',5,mode='rtu')
# instrument.debug= True
abc  =  instrument.read_registers(3,16,3)
print (abc[0])
print (abc[1])
print (abc[2])
print (abc[3])
print (abc[4])
print (abc[5])
print (abc[6])
print (abc[7])
print (abc[8])
print (abc[9])
print (abc[10])
print (abc[11])
print (abc[12])
print (abc[13])
print (abc[14])
print (abc[15])