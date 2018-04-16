import minimalmodbus
import serial
import time
import numpy as np
import statistics
from pyModbusTCP.client import ModbusClient

#Define Communication parameters
minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1
#not closing port after each call causes buffer overflow issue(Probably?)
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

# TCP auto connect on first modbus request
c = ModbusClient(host="localhost", port=502, auto_open=True)

# TCP auto connect on modbus request, close after it
c = ModbusClient(host="127.0.0.1", auto_open=True, auto_close=True)

c = ModbusClient()
c.host("localhost")
c.port(502)
# managing TCP sessions with call to c.open()/c.close()
c.open()

#Read 2x 16 bits registers at modbus address 0 :
regs = c.read_holding_registers(0,2)
if regs:
 print(regs)
else:
 print("read error")

 
#Write value 44 and 55 to registers at modbus address 10 :
if c.write_multiple_registers(10,[44,55]):
 print("write ok")
else:
 print("write error")
 
data1 = np.zeros(16)
data2 = np.zeros(16)
data3 = np.zeros(8)
d