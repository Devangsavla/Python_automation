from tkinter import *
import subprocess
from PIL import ImageTk, Image
import sys
import os

nodex = Tk()
nodex.title("NodeX Testing")
nodex.configure(background = "white")
#nodex.iconbitmap('susten_logo.ico')

port_no_1 = "test"
test_mode = IntVar()

def exit():
	sys.exit()

def refresh():
	python = sys.executable
	os.execl(python, python, * sys.argv)
	# subprocess.run("py gui_nodex.py")
	#os.system("py gui_nodex.py")
	sys.exit()

def find_port():
	port_no_1 = subprocess.check_output('plink pi@10.10.10.228 -pw mpulse@123 "python NodexTest.py 2222 TRUE portset?"').decode("utf-8")
	print("Port Number: ",port_no_1)
	c3_2.configure(text = port_no_1)

def test_main():
	#Add command line
	port_no_2 = c6_2.get()
	print(port_no_2)
	if (test_mode.get() == 0):
		print("Normal Mode")
		testing_cmd = 'plink -v pi@10.10.10.228 -pw mpulse@123 "python NodexTest.py '+port_no_2+'"'
		testing_output = subprocess.check_output(testing_cmd).decode("utf-8")
		
	if (test_mode.get() == 1):
		print("Debug Mode")
		testing_cmd = 'plink -v pi@10.10.10.228 -pw mpulse@123 "python NodexTest.py '+port_no_2+' TRUE"'
		testing_output = subprocess.check_output(testing_cmd).decode("utf-8")

	output_list = [x.strip() for x in testing_output.split(',')]
	print(output_list)
	c10_1.configure(text = testing_output)

def datalog():
	print("Data log")

grid_width = 25

#Row 0
# susten_logo = PhotoImage(file = "susten_logo.gif")
# susten_logo = susten_logo.subsample()
# c0 = Label(nodex, image = susten_logo, bg = "grey", fg = "black")
# c0.grid(row = 0, column = 1, sticky = N+E+W+S, columnspan = 3)

#Row 1
c1_1 = Label(nodex, bg = "white")
c1_1.grid(row = 1, column = 1, sticky = W)

#Row 2
c2_1 = Label(nodex, text="Testing setup:", width=grid_width, bg = "white", fg = "black")
c2_1.grid(row = 2, column = 1, sticky = W)

#Row 3
c3_1 = Button(nodex, text = "Find Port Number>", width=grid_width, command=find_port)
c3_1.grid(row = 3, column = 1, sticky = W)
c3_2 = Label(nodex, text = port_no_1, width=grid_width,bg ="white", fg = "black")
c3_2.grid(row = 3, column = 2, sticky = W, columnspan = 2)

#Row 4
c4_1 = Label(nodex, width=grid_width, bg = "white", fg = "black")
c4_1.grid(row = 4, column = 1, sticky = W)

#Row 5
c5_1 = Label(nodex, text="Testing:", width=grid_width, bg = "white", fg = "black")
c5_1.grid(row = 5, column = 1, sticky = W)

#Row 6
c6_1 = Label(nodex, text="Enter Port Number", width = grid_width, bg = "white", fg = "black")
c6_1.grid(row = 6, column = 1, sticky = W)
c6_2 = Entry(nodex, width = 24,bg = "white", bd = 1)
c6_2.grid(row = 6, column = 2, sticky = W)
c6_3 = Checkbutton(nodex, text="Debug Mode", width = 12, variable=test_mode, bg = "white")
c6_3.grid(row = 6, column = 3, sticky = W)

#Row 7
c7_3 = Button(nodex, text = "Begin Test>", width=grid_width, command=test_main)
c7_3.grid(row = 7, column = 2, sticky = W)

#Row 8
c8_1 = Label(nodex, bg = "white")
c8_1.grid(row = 8, column = 1, sticky = W)

#Row 9
c9_1 = Label(nodex, text="Testing data:", width=grid_width, bg = "white", fg = "black")
c9_1.grid(row = 9, column = 1, sticky = W)

#Row 10
c10_1 = Label(nodex, width = grid_width*3, height = 6, bg = "white")
c10_1.grid(row = 10, column = 1, sticky = W, columnspan=3)

#Row 11
c11_1 = Label(nodex, text = "Testing Output:",width = grid_width, bg = "white")
c11_1.grid(row = 11, column = 1, sticky = W)

#Row 12
c12_1 = Label(nodex, text = "NodeX ID:", bg = "white", width=grid_width, fg = "black")
c12_1.grid(row = 12, column = 1, sticky = W)
c12_2 = Label(nodex, bg = "white", width=30, fg = "black")
c12_2.grid(row = 12, column = 2, sticky = W, columnspan = 2)

#Row 13
c13_1 = Label(nodex, text = "Ethernet MAC:", bg = "white", width=grid_width, fg = "black")
c13_1.grid(row = 13, column = 1, sticky = W)
c13_2 = Label(nodex, bg = "white", width=30, fg = "black")
c13_2.grid(row = 13, column = 2, sticky = W, columnspan = 2)

#Row 14
c14_1 = Label(nodex, text = "Wifi MAC:", bg = "white", width=grid_width, fg = "black")
c14_1.grid(row = 14, column = 1, sticky = W)
c14_2 = Label(nodex, bg = "white", width=grid_width*2, fg = "black")
c14_2.grid(row = 14, column = 2, sticky = W, columnspan = 2)

#Row 15
c15_1 = Label(nodex, text = "Sim IMEI", bg = "white", width=grid_width, fg = "black")
c15_1.grid(row = 15, column = 1, sticky = W)
c15_2 = Label(nodex, bg = "white", width=grid_width*2, fg = "black")
c15_2.grid(row = 15, column = 2, sticky = W, columnspan = 2)

#Row 16
c16_1 = Label(nodex, text = "RS485 Status", bg = "white", width=grid_width, fg = "black")
c16_1.grid(row = 16, column = 1, sticky = W)
c16_2 = Label(nodex, bg = "white", width=grid_width*2, fg = "black")
c16_2.grid(row = 16, column = 2, sticky = W, columnspan = 2)

#Row 17
c17_1 = Label(nodex, bg = "white")
c17_1.grid(row = 17, column = 1, sticky = W)

#Row 18
c18_1 = Label(nodex, text = "Final Status", bg = "white", width=grid_width, fg = "black")
c18_1.grid(row = 18, column = 1, sticky = W)
c18_2 = Button(nodex, text = "Save Data", width=grid_width, fg = "black", command = datalog)
c18_2.grid(row = 18, column = 2, sticky = W)

#Row 20
c20_3 = Button(nodex, text = "Refresh", width=grid_width, command=refresh)
c20_3.grid(row = 20, column = 1, sticky = W)
c20_3 = Button(nodex, text = "Exit", width=grid_width, command=exit)
c20_3.grid(row = 20, column = 3, sticky = W)

nodex.mainloop()