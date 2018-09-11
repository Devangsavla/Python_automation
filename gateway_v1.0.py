import serial
import socket
import sys
import minimalmodbus
import time
from umodbus.client.serial import rtu

# Function to display host name and IP address
def get_Host_name_IP():
	try:
		host_name = socket.gethostname()
		host_ip = socket.gethostbyname(host_name)
		print("Hostname: ",host_name)
		print("Host IP:  ",host_ip)
	except:
		print("Unable to get Host name and IP")

#Function takes in tcp request, processes in rtu and sends back tcp reply
def modbus_tcp_rtu(data_in):
	def msb(data):
		return (data // 256)

	def lsb(data):
		return (data % 256)

	def combine_msb_lsb(data_msb,data_lsb):
		return ((data_msb*256)+data_lsb)

	com_port = '/dev/ttyUSB0'
	slave_id = data_in[6]
	func = data_in[7]
	str_add = combine_msb_lsb(data_in[8],data_in[9])
	no_of_regs = combine_msb_lsb(data_in[10],data_in[11])

	if (func == 1) or (func == 2):
		#Round up the number of registers without external function
		coil_bytes = -(-no_of_regs//8)
		data_out = [0]*(9 + coil_bytes)
		data_out[8] = coil_bytes

		ser1 = serial.Serial(
		 port = com_port,
		 baudrate = 9600,
		 parity = serial.PARITY_NONE,
		 stopbits = serial.STOPBITS_ONE,
		 bytesize = serial.EIGHTBITS,
		 timeout = 1
		 )

		coil_request = rtu.read_coils(slave_id, str_add, no_of_regs)
		coil_request = rtu.read_coils(1, 0, 10)

		ser1.write(bytes(coil_request))
		time.sleep(0.1)
		while ser1.inWaiting():
			coil_reply = ser1.readline()
		data_out[9:] = coil_reply[3:-2]

	
	if (func == 3) or (func == 4):
		data_out = [0]*((2*data_in[11]) + 9)
		data_out[8] = data_in[11]*2
		#Define Modbus Parameters
		minimalmodbus.BAUDRATE= 9600
		minimalmodbus.BYTESIZE = 8
		minimalmodbus.PARITY= 'N'
		minimalmodbus.STOPBITS = 1
		minimalmodbus.TIMEOUT = 1
		
		#not closing port after each call causes buffer overflow issue(Probably?)
		minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

		gw = minimalmodbus.Instrument(com_port,slave_id,mode='rtu')
		gw.debug= False

		if no_of_regs == 1:
			rtu_data_out = gw.read_register(str_add, 0, func)
			data_out[9] = msb(rtu_data_out)
			data_out[10] = lsb(rtu_data_out)

		else:
			rtu_data_out = gw.read_registers(str_add, no_of_regs, func)
			for i in range(len(rtu_data_out)):
				data_out[9 + 2*i] = msb(rtu_data_out[i])
				data_out[9 + 2*i + 1] = lsb(rtu_data_out[i])

	data_out[0] = data_in[0]
	data_out[1] = data_in[1]
	data_out[2] = data_in[2]
	data_out[3] = data_in[3]
	data_out[4] = msb((2*data_in[11]) + 3)
	data_out[5] = lsb((2*data_in[11]) + 3)
	data_out[6] = slave_id
	data_out[7] = func

	return data_out

#Get System details
get_Host_name_IP() 

#Create a TCP/IP socket
try:
	#Address domain types:
	#Unix domain 		>> AF_UNIX >> 2 processes which share common file system
	#Internet domain	>> AF_INET >> Any 2 hosts on the Internet 
	
	#Socket types
	#A stream socket 	>> Characters are read in a continuous stream as if from a file or pipe
	#A datagram socket 	>> Characters are read in chunks.

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# The SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire.
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print("Socket created!!")
except socket.error as e:
	print("Failed to create socket! Error Message: ",e)
	sys.exit()

#define host and port
host = '' #Receive packets from all network interface
port = 502

#Bind host and port.Bind at server. Connect at client.
try:
	s.bind((host,port))
except socket.error as e:
	print(str(e))
	sys.exit()

s.listen(5)
print("Waiting for a connection")

while True:
	#addr is a pointer to a sockaddr structure
	conn,addr = s.accept()
	print('Connected to: ' + str(addr[0])) # + ':' + str(addr[1]))
	conn.send(str.encode("Welcome: \n"))
	while True:
		try:	
			request = list(conn.recv(2048))
			if not request:
				break
			print("Request : ",request)
			reply = modbus_tcp_rtu(request)
			print("Reply : ",reply,"\n")
			#Sendall will send everything or will through error.
			conn.sendall(bytes(reply))
		except KeyboardInterrupt:
			print("\r  ")
			print("OK bye!")
			sys.exit()
	conn.close()
