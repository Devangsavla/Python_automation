from tkinter import *
import tkinter.scrolledtext as tkst
from tkinter import font
import subprocess
import sys
import os
import datetime

sr_no = input('Enter NodeX Serial Number: ')

sr_no_text = "Serial No: "+sr_no

nodex = Tk()
nodex.title("NodeX Testing")
nodex.configure(background = "white")
#nodex.iconbitmap('susten_logo.ico')
nodex.state('zoomed')

port_no_1 = "0"
test_mode = IntVar()

font_size = 5
grid_width = 30	

def exit():
	sys.exit()

def refresh():
	python = sys.executable
	os.execl(python, python, * sys.argv)
	sys.exit()

def find_port():
	port_no_1 = subprocess.check_output('plink pi@192.168.1.220 -pw mpulse@123 "python NodexTest.py 2222 True portset?"').decode("utf-8")
	print("Port Number: ",port_no_1)
	c3_2.configure(text = port_no_1)

def test_main():
	global dt
	dt = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
	print("button pressed")
	c10_1.delete(1.0,END)
	port_no_2 = c6_2.get()
	
	print(port_no_2)
	global output_list
	try:
		num_chk = (3000 <= int(port_no_2) <= 9999)
	except:
		print("Invalid Entry. Enter a valid number")
		c10_1.insert(INSERT,"Invalid Entry. Enter a valid number")
		num_chk = None

	if(num_chk == True):	
		global output_list
		if (test_mode.get() == 0):
			print("Normal Mode")
			testing_cmd = 'plink -v pi@192.168.1.220 -pw mpulse@123 "python NodexTest.py '+port_no_2+'"'
			testing_output = subprocess.check_output(testing_cmd).decode("utf-8")
			output_list = [x.strip() for x in testing_output.split(',')]
		
		if (test_mode.get() == 1):
			print("Debug Mode")
			testing_cmd = 'plink -v pi@192.168.1.220 -pw mpulse@123 "python NodexTest.py '+port_no_2+' True"'
			testing_output = subprocess.check_output(testing_cmd).decode("utf-8")
			temp_list = testing_output.partition('| Tested ok |')
			testing_output2 = temp_list[2]
			output_list = [x.strip() for x in testing_output2.split(',')]
	
		print(str(output_list))
		# c10_1.configure(text = testing_output)
		c10_1.insert(INSERT,testing_output)
		if len(output_list) > 2:
			c12_2.configure(text = output_list[0])
			c13_2.configure(text = output_list[1])
			c14_2.configure(text = output_list[2])
			c15_2.configure(text = output_list[3])
			c16_2.configure(text = "hello")

			if output_list[1] != 0:
				c13_3.configure(bg = "green", text = "Ethernet Pass")
			if output_list[1] == 0:
				c13_3.configure(bg = "red", text = "Ethernet Fail")

			if output_list[4] == 'True':
				c14_3.configure(bg = "green", text = "Wifi Pass")
			if output_list[4] == 'False':
				c14_3.configure(bg = "red", text = "Wifi Fail")

			if output_list[6] == 'True':
				c15_3.configure(bg = "green", text = "GSM Pass")
			if output_list[6] == 'False':
				c15_3.configure(bg = "red", text = "GSM Fail")

			if output_list[5] == 'True':
				c16_3.configure(bg = "green", text = "RS485 Pass")
			if output_list[5] == 'False':
				c16_3.configure(bg = "red", text = "RS485 Fail")	

			if output_list[7] == 'Pass':
				c18_3.configure(bg = "green", text = "Final Pass")
			if output_list[7] == 'Fail':
				c18_3.configure(bg = "red", text = "Final Fail")
	elif(num_chk == False):
		print("Invalid Port Number. Valid range is between 3000 to 9999")
		c10_1.insert(INSERT,"Invalid Port Number. Valid range is between 3000 to 9999")

def datalog():
	print("Data log")
	target = open("nodex_log.csv","a")
	target.write(str(dt))
	target.write(',')
	target.write(str(sr_no))
	target.write(',')
	for i in range(8):
		target.write(output_list[i])
		target.write(",")
	target.write('\n')
	target.close()

def ping_nodex():
	rep = os.system('ping -n 1 192.168.1.220 | find "TTL="')
	print(rep)
	if rep == 0:
		c3_3.configure(bg = "green")
		c7_3.configure(state = NORMAL)
	else:
		c3_3.configure(bg = "red")	

#Row 1
c1_1 = Label(nodex, bg = "white", font = font_size)
c1_1.grid(row = 1, column = 1, sticky = W)

#Row 2
c2_1 = Label(nodex, text="Testing:", width=grid_width, bg = "white", fg = "black", font = font_size)
c2_1.grid(row = 2, column = 1, sticky = W)
c2_3 = Label(nodex, text=sr_no_text, width=grid_width, bg = "white", fg = "black", font = font_size)
c2_3.grid(row = 2, column = 3, sticky = W)

#Row 3
c3_1 = Button(nodex, text = "Find Port Number>", width=grid_width, command=find_port, font = font_size)
c3_1.grid(row = 3, column = 1, sticky = W)
c3_2 = Label(nodex, text = port_no_1, width=grid_width,bg ="white", fg = "black", font = font_size)
c3_2.grid(row = 3, column = 2, sticky = W)
c3_3 = Button(nodex, text = "Ping NodeX", width=grid_width, command=ping_nodex, font = font_size)
c3_3.grid(row = 3, column = 3, sticky = W)

#Row 4
c4_1 = Label(nodex, width=grid_width, bg = "white", fg = "black", font = font_size)
c4_1.grid(row = 4, column = 1, sticky = W)

#Row 5
c5_1 = Label(nodex, text="Testing:", width=grid_width, bg = "white", fg = "black", font = font_size)
c5_1.grid(row = 5, column = 1, sticky = W)

#Row 6
c6_1 = Label(nodex, text="Enter Port Number", width = grid_width, bg = "white", fg = "black", font = font_size)
c6_1.grid(row = 6, column = 1, sticky = W)
c6_2 = Entry(nodex, width = 24,bg = "white", bd = 1, font = font_size)
c6_2.grid(row = 6, column = 2, sticky = W)
c6_3 = Checkbutton(nodex, text="Debug Mode", width = 12, variable=test_mode, bg = "white", font = font_size)
c6_3.grid(row = 6, column = 3, sticky = W)

#Row 7
c7_3 = Button(nodex, text = "Begin Test>", width=grid_width, command=test_main, state = DISABLED, font = font_size)
c7_3.grid(row = 7, column = 2, sticky = W)

#Row 8
c8_1 = Label(nodex, bg = "white", font = font_size)
c8_1.grid(row = 8, column = 1, sticky = W)

#Row 9
c9_1 = Label(nodex, text="Testing data:", width=grid_width, bg = "white", fg = "black", font = font_size)
c9_1.grid(row = 9, column = 1, sticky = W)

#Row 10
c10_1 = tkst.ScrolledText(nodex, width = grid_width*3, height = 10, bg = "white", font = font_size)
c10_1.grid(row = 10, column = 1, columnspan = 3)

#Row 11
c11_1 = Label(nodex, text = "Testing Output:",width = grid_width, bg = "white", font = font_size)
c11_1.grid(row = 11, column = 1, sticky = W)

#Row 12
c12_1 = Label(nodex, text = "NodeX ID:", bg = "white", width=grid_width, fg = "black", font = font_size)
c12_1.grid(row = 12, column = 1, sticky = W)
c12_2 = Label(nodex, bg = "white", width=grid_width, fg = "black", font = font_size)
c12_2.grid(row = 12, column = 2, sticky = W)

#Row 13
c13_1 = Label(nodex, text = "Ethernet MAC:", bg = "white", width=grid_width, fg = "black", font = font_size)
c13_1.grid(row = 13, column = 1, sticky = W)
c13_2 = Label(nodex, bg = "white", width=grid_width, fg = "black", font = font_size)
c13_2.grid(row = 13, column = 2, sticky = W)
c13_3 = Label(nodex, bg = "white", width=grid_width, fg = "black", font = font_size)
c13_3.grid(row = 13, column = 3, sticky = W)

#Row 14
c14_1 = Label(nodex, text = "Wifi MAC:", bg = "white", width=grid_width, fg = "black", font = font_size)
c14_1.grid(row = 14, column = 1, sticky = W)
c14_2 = Label(nodex, bg = "white", width=grid_width, fg = "black", font = font_size)
c14_2.grid(row = 14, column = 2, sticky = W)
c14_3 = Label(nodex, bg = "white", width=grid_width, fg = "black", font = font_size)
c14_3.grid(row = 14, column = 3, sticky = W)

#Row 15
c15_1 = Label(nodex, text = "GSM IMEI", bg = "white", width=grid_width, fg = "black", font = font_size)
c15_1.grid(row = 15, column = 1, sticky = W)
c15_2 = Label(nodex, bg = "white", width=grid_width, fg = "black", font = font_size)
c15_2.grid(row = 15, column = 2, sticky = W)
c15_3 = Label(nodex, bg = "white", width=grid_width, fg = "black", font = font_size)
c15_3.grid(row = 15, column = 3, sticky = W)

#Row 16
c16_1 = Label(nodex, text = "RS485 Status", bg = "white", width=grid_width, fg = "black", font = font_size)
c16_1.grid(row = 16, column = 1, sticky = W)
c16_2 = Label(nodex, bg = "white", width=grid_width, fg = "black", font = font_size)
c16_2.grid(row = 16, column = 2, sticky = W)
c16_3 = Label(nodex, bg = "white", width=grid_width, fg = "black", font = font_size)
c16_3.grid(row = 16, column = 3, sticky = W)

#Row 17
c17_1 = Label(nodex, bg = "white", font = font_size)
c17_1.grid(row = 17, column = 1, sticky = W)

#Row 18
c18_2 = Label(nodex, text = "Final Status", bg = "white", width=grid_width, fg = "black", font = font_size)
c18_2.grid(row = 18, column = 2, sticky = W)
c18_3 = Label(nodex, bg = "white", width=grid_width, fg = "black", font = font_size)
c18_3.grid(row = 18, column = 3, sticky = W)

c19_3 = Button(nodex, text = "Save Data", width=grid_width, fg = "black", command = datalog, font = font_size)
c19_3.grid(row = 19, column = 3, sticky = W)

#Row 20
c20_3 = Button(nodex, text = "Refresh", width=grid_width, command=refresh, font = font_size)
c20_3.grid(row = 20, column = 1, sticky = W)
c20_3 = Button(nodex, text = "Exit", width=grid_width, command=exit, font = font_size)
c20_3.grid(row = 20, column = 3, sticky = W)

nodex.mainloop()