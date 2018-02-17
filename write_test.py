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

m = np.zeros(16)
c = np.zeros(16)
vm = 10000
vc = 10

smb = minimalmodbus.Instrument('COM15',3,mode='rtu')
smb.debug= True

smb.write_registers(0,[int(m[0]),int(m[1]),int(m[2]),int(m[3]),int(m[4]),int(m[5]),int(m[6]),int(m[7]),int(m[8]),int(m[9]),int(m[10]),int(m[11]),int(m[12]),int(m[13]),int(m[14]),int(m[15]),int(c[0]),int(c[1]),int(c[2]),int(c[3]),int(c[4]),int(c[5]),int(c[6]),int(c[7]),int(c[8]),int(c[9]),int(c[10]),int(c[11]),int(c[12]),int(c[13]),int(c[14]),int(c[15]),int(vm),int(vc)])
print("writing done")