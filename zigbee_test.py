import serial
from xbee import XBee

serial_port = serial.Serial('COM4', 9600)
xbee = XBee(serial_port)

while(1):
 try:
  print xbee.wait_read_frame()
 except KeyboardInterrupt:
  break
serial_port.close()