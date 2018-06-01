import minimalmodbus

#Define Modbus Parameters
minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1
#not closing port after each call causes buffer overflow issue(Probably?)
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

#Define PCB Parameters
smb = minimalmodbus.Instrument('COM3',3,mode='rtu')
smb.debug= False

while True:
	print(smb.read_registers(3,8,3))