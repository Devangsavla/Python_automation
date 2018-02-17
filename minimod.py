import serial
import time
import nidaqmx
import nidaqmx.system

system = nidaqmx.system.System.local()
system.driver_version
DriverVersion(major_version=16L, minor_version=0L, update_version=0L)
for device in system.devices:
 print(device)

for i in range(0,8):
 ch = 'Dev1/ai' + str(i)
 print ch
 with nidaqmx.Task() as task:
  task.ai_channels.add_ai_voltage_chan(ch)
  ref = task.read()
  print("Channel%d: "%i),ref