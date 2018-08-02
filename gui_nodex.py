from tkinter import *
from subprocess import call
from PIL import ImageTk,Image  

nodex = Tk()
nodex.title("NodeX Testing")
nodex.configure(background = "white")
#nodex.iconbitmap('susten_logo.ico')

port_no_1 = "test"

def exit():
	exit()

def find_port():
	#Add command line
	print("Command for finding port is executed.")
	port_no_1 = "OK"
	c3_2.configure(text = port_no_1)
	
def test_main():
	#Add command line
	if (test_mode.get() == 1):
		print("Normal Mode")
	if (test_mode.get() == 2):
		print("Debug Mode")	
	port_no_2 = c6_2.get()
	print(port_no_2)


#Row 0
susten_logo = PhotoImage(file = "sustenlogo.gif")
c0 = Label(nodex, image = susten_logo, bg = "white", fg = "black")
c0.grid(row = 0, column = 2, sticky = W)

#Row 1
c1_1 = Label(nodex, bg = "white")
c1_1.grid(row = 1, column = 1, sticky = W)

#Row 2
c2_1 = Label(nodex, text="Testing setup:", width=14, bg = "white", fg = "black")
c2_1.grid(row = 2, column = 1, sticky = W)

#Row 3
c3_1 = Button(nodex, text = "Find Port Number>", width=17, command=find_port)
c3_1.grid(row = 3, column = 1, sticky = W)
c3_2 = Label(nodex, text = port_no_1, bg = "white", width=10, fg = "black")
c3_2.grid(row = 3, column = 2, sticky = W)

#Row 4
c4_1 = Label(nodex, width=14, bg = "white", fg = "black")
c4_1.grid(row = 4, column = 1, sticky = W)

#Row 5
c5_1 = Label(nodex, text="Testing:", width=8, bg = "white", fg = "black")
c5_1.grid(row = 5, column = 1, sticky = W)

#Row 6
c6_1 = Label(nodex, text="Enter Port Number for Testing", width=30	, bg = "white", fg = "black")
c6_1.grid(row = 6, column = 1, sticky = W, columnspan=2)
c6_2 = Entry(nodex)
c6_2.grid(row = 6, column = 3, sticky = W)

#Row 7
test_mode = IntVar()
c7_1 = Radiobutton(nodex, text='Normal', variable=test_mode, value=1)
c7_1.grid(row = 7, column = 1, sticky = W)
c7_2 = Radiobutton(nodex, text='Debug', variable=test_mode, value=2)
c7_2.grid(row = 7, column = 2, sticky = W)
c7_3 = Button(nodex, text = "Begin Test>", width=17, command=test_main)
c7_3.grid(row = 7, column = 3, sticky = W)

nodex.mainloop()