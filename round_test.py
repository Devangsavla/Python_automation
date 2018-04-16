import minimalmodbus
import serial
import time
import numpy as np
import statistics
import nidaqmx

vx = np.zeros(3)
vy = np.zeros(3)
# d = np.zeros(16)
# c = np.zeros(16)

#function whose input is x & y lists and output is m & c lists
def regression(x_s,y_s):
 # mean of all elements
 # dividing by 10 to avoid overflow in calculation
 x_mean= 0.1*statistics.mean(x_s)
 y_mean= 0.1*statistics.mean(y_s)

 # square every element
 x2=0.1*0.1*x_s*x_s
 x2_mean = statistics.mean(x2)

 # element wise multiplication of 2 list
 xy=0.1*0.1*x_s*y_s
 xy_mean = statistics.mean(xy)

 # regression calculation
 # not multiplying 10 back as it gets canceled in Nr and Dr
 m = ((x_mean * y_mean) - xy_mean)/((x_mean*x_mean) - x2_mean)
 m=round(m,4)
 # multiplying back by 10 
 c = 10*(y_mean - (x_mean*m))
 c = round(c)
 # c = c-20
 return m,c

raw_input("Set Voltage to 300V and PRESS ENTER")
vx[0]= raw_input("Enter pcb voltage value and press ENTER: ")
print("PCB voltage 1: "),vx[0]
vy[0] = raw_input("Enter Fluke voltage value and press ENTER: ")
print("Multimeter voltage 1: "),vy[0]

raw_input("Set Voltage to 500V and PRESS ENTER")
vx[1]= raw_input("Enter pcb voltage value and press ENTER: ")
print("PCB voltage 2: "),vx[1]
vy[1] = raw_input("Enter Fluke voltage value and press ENTER: ")
print("Multimeter voltage 2: "),vy[1]

raw_input("Set Voltage to 900V and PRESS ENTER")
vx[2]= raw_input("Enter pcb voltage value and press ENTER: ")
print("PCB voltage 3: "),vx[2]
vy[2] = raw_input("Enter Fluke voltage value and press ENTER: ")
print("Multimeter voltage 3: "),vy[2]

# vm = raw_input("Enter Voltage M: ")
# print("voltage m: "),vm
# vc = raw_input("Enter Voltage C: ")
# print("voltage c: "),vc
# vm=9140
# vc=2

vm,vc = regression(vx,vy)
vm = int(vm*10000)
vc = int(vc)

print("VM: "),int(vm)
print("VC: "),int(vc)
