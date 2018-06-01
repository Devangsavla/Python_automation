import socket
import sys
import minimalmodbus

#Define Modbus Parameters
minimalmodbus.BAUDRATE= 9600
minimalmodbus.BYTESIZE = 8
minimalmodbus.PARITY= 'N'
minimalmodbus.STOPBITS = 1
minimalmodbus.TIMEOUT = 1
#not closing port after each call causes buffer overflow issue(Probably?)
minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True

slave_id = 1

#Define PCB Parameters
smb = minimalmodbus.Instrument('/dev/ttyUSB0',slave_id,mode='rtu')
smb.debug= False

#define host and port
host = '' #Receive packets from all network interface
port = 5555

# Function to display hostname and IP address
def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print("Hostname :  ",host_name)
        print("IP : ",host_ip)
    except:
        print("Unable to get Host name and IP")

def modbus(x):
	packet_no = x[0]
	rtu_length = x[5]
	slave_id = x[6]
	func_code = x[7]
	start_add = (x[8]*256) + x[9]
	no_of_regs = (x[10]*256) + x[11]
	
	if x[5] != 6:
		print("Invalid Request")
	print("Slave ID:",slave_id,"   Function Code:",func_code,"   Starting address:",start_add,"   No of Registers:",no_of_regs,end='\r')
		
	if no_of_regs == 1:
		if func_code == 2:
			x = smb.read_bit(start_add,func_code)
		if func_code == 4:
			x = smb.read_register(start_add,0,func_code)
	
	else:
		x = smb.read_registers(start_add,no_of_regs,func_code)
	
	return x

#Get System details
#get_Host_name_IP() 

#Create a TCP/IP socket
#Address domain types:
	#Unix domain >> AF_UNIX >> 2 processes which share common file system
	#Internet domain>> AF_INET >> Any 2 hosts on the Internet 
#A stream socket in which characters are read in a continuous stream as if from a file or pipe, and a datagram socket, in which messages are read in chunks.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire.
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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
	print('connected to: ' + str(addr[0])) # + ':' + str(addr[1]))
	conn.send(str.encode("Welcome: \n"))
	while True:
		try:	
			request = conn.recv(2048)
			if not request:
				break
			data = list(request)		
			reply = str(data)
			#reply = str(modbus(data))
			conn.sendall(reply.encode('utf-8'))
		except KeyboardInterrupt:
			print("\r  ")
			print("OK bye!")
			sys.exit()
	conn.close()