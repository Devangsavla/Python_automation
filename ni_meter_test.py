import serial
import time
import nidaqmx
import nidaqmx.system
import numpy as np

y = np.zeros(8)
while(1):
#function to read 8 channel voltage from NI card
 # for i in range(0,1):
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
  y=(y*100000)+50
  time.sleep(2)
 print(y)