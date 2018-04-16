from pyModbusTCP.client import ModbusClient
import time

try:
 c = ModbusClient(host= "localhost", port= 502) 
 
except ValueError:
 print("Error with host or port parameters")

while(1):
 if not c.is_open():
  if not c.open():
   print("unable to connect to ")
 if c.is_open():
  hreg = c.read_holding_registers(0,10)
  creg = c.read_coils(0,5)
 
 if hreg:
  print("Holding registers 0 to 9:"+str(hreg))
  
 if creg:
  print("Coil registers 0 to 4:"+str(creg))
  time.sleep(1)
  
# uncomment this line to see debug message
# c.debug(True)

# while True:
    # # open or reconnect TCP to server
    # if not c.is_open():
        # if not c.open():
            # print("unable to connect to ")

    # # if open() is ok, read register (modbus function 0x03)
    # if c.is_open():
        # # read 10 registers at address 0, store result in regs list
        # regs = c.read_holding_registers(0, 10)
        # # if success display registers
        # if regs:
            # print("reg ad #0 to 9: "+str(regs))

    # # sleep 2s before next polling
    # time.sleep(1)