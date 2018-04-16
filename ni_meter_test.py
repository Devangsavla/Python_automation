import serial
import time
import nidaqmx
import nidaqmx.system

while(1):
 ch = 'Dev1/ai0'
 
 with nidaqmx.Task() as task:
  task.ai_channels.add_ai_voltage_chan(ch, max_val=+0.04, min_val=-0.01)
  y = task.read()
  y = y + task.read()
  y = y + task.read()
  y = y + task.read()
  y = y + task.read()
  y = y + task.read()
  y = y + task.read()
  y = y + task.read()
  y = y + task.read()
  y = y + task.read()
  y=(y/10)
  time.sleep(2)
 print(y)