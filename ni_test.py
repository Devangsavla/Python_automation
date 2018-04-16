import serial
import time
import nidaqmx
import nidaqmx.system
import numpy as np

def nidata():
 for i in range(0,8):
  ch = 'Dev1/ai' + i
  with nidaqmx.Task() as task:
   # task.ai_channels.add_ai_voltage_chan(ch)
   task.ai_channels.add_ai_voltage_chan(ch, max_val=0.1, min_val=-0.1)
   time.sleep(1)
   y = task.read(number_of_samples_per_channel=8)
 return(y)

while(1):
 # y = np.zeros(2)
 y = nidata()
 print(y)
 time.sleep(0.1)



# for i in range(0,8):
 # ch = 'Dev1/ai' + str(i)
 # with nidaqmx.Task() as task:
  # task.ai_channels.add_ai_voltage_chan(ch)
  # y[i] = task.read()

# def niread():
 # for i in range(0,8):
  # ch = 'Dev1/ai' + str(i)
  # print ch
  # with nidaqmx.Task() as task:
   # task.ai_channels.add_ai_voltage_chan(ch)
   # ref = task.read()
   # print(ref)
  
# with nidaqmx.Task() as task:
 # task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
 # ref = task.read()
 # print(ref)
 # task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
 # ref = task.read()
 # print(ref) 
 # task.ai_channels.add_ai_voltage_chan("Dev1/ai2")
 # ref = task.read()
 # print(ref) 
 # task.ai_channels.add_ai_voltage_chan("Dev1/ai3")
 # ref = task.read()
 # print(ref) 
 # task.ai_channels.add_ai_voltage_chan("Dev1/ai4")
 # ref = task.read()
 # print(ref)  