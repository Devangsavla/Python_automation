import socket
import minimalmodbus
import sys
import numpy as np

#Define Modbus Parameters
minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1
#not closing port after each call causes buffer overflow issue(Probably?)
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

#define host and port
host = '' #Receive packets from all network interface
port = 3333

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# def modbus(data):
	# packet_no = data[0]
	# rtu_length = data[5]
	# slave_id = data[6]
	# func_code = data[7]
	# start_add = (data[8]*256) + data[9]
	# no_of_regs = (data[10]*256) + data[11]
	# reply_length = (no_of_regs) + 9
	# x = np.zeros(reply_length)
	# #Define PCB Parameters
	# smb = minimalmodbus.Instrument('/dev/ttyUSB0',(slave_id),mode='rtu')
	# smb.debug= False
	
	# if data[5] != 6:
		# print("Invalid Request")
		
	# if no_of_regs == 1:
		# if func_code == 2:
			# x = smb.read_bit(start_add,2)
		# if func_code == 1:
			# x = smb.read_bit(start_add,1)
		# if func_code == 4:
			# x = smb.read_register(start_add,0,4)
	
	# else:
		# x = smb.read_registers(start_add,no_of_regs,func_code)
	# reply = list(data[:4]) + [0] + [0] + [0] + [0] + [0] + x + [0] + [0] + [0] + [0] + [0]
	# m_len = (no_of_regs)*2 + 3
	# d_len = (no_of_regs)*2
	# reply[4] = (m_len)//256
	# reply[5] = (m_len)%256
	# reply[6] = data[6]
	# reply[7] = data[7]
	# reply[8] = no_of_regs*2
	# return reply

def modbus(req):
	str_add = req[8]*256 + req[9]
	no_of_regs = req[10]*256 + req[11]
	slave_id = req[6]
	func_code = req[7]
	rep_len = no_of_regs*2 + 3
	reply = [0]*9
	reply[0] = req[0]
	reply[1] = req[1]
	reply[2] = req[2]
	reply[3] = req[3]
	reply[4] = (rep_len//256)
	reply[5] = (rep_len%256)
	reply[6] = req[6]
	reply[7] = req[7]
	reply[8] = (rep_len - 3)%256
	print("initial reply: ",reply)
	smb = minimalmodbus.Instrument('/dev/ttyUSB0',(slave_id),mode='rtu')
	smb.debug= False
	
	if req[5] != 6:
		print("Invalid Request")
		
	if no_of_regs == 1:
		if func_code == 2:
			x = smb.read_bit(str_add,2)
		if func_code == 1:
			x = smb.read_bit(str_add,1)
		if func_code == 4:
			x = smb.read_register(str_add,0,4)
	
	else:
		x = smb.read_registers(str_add,no_of_regs,func_code)
	print("n element list: ",x)
	rep = [None]*(2*len(x))
	
	for i in range(len(x)):
		rep[2*i] = x[i]//256
		rep[(2*i)+1] = x[i]%256
	print("2n element list: ",rep)
	reply = reply + rep
	print("final reply: ",reply)
	return reply	

try:
	s.bind((host,port))
except socket.error as e:
	print(str(e))
	sys.exit()
	
s.listen(5)
print("Waiting for a connection")

while True:
	#conn is a new socket object usable to send and receive data on the connection, and address is the address bound to the socket on the other end of the connection.

	conn,addr = s.accept()
	print('connected to: ' + str(addr[0])) # + ':' + str(addr[1]))
	conn.send(str.encode("Lets go!"))
	while True:
		try:	
			request = conn.recv(2048)
			if not request:
				break
			print("request:	",list(request))
			reply = modbus(request)
			print("reply:	",reply)
			conn.sendall(bytes(reply))
		except KeyboardInterrupt:
			print("\r  ")
			print("Quit")
			sys.exit()
	conn.close()