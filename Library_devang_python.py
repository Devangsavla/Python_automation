

#quotient & remainder
c = a/b #Quotient
c = a%b #Remainder

#How to calculate program run time
import time
start_time = time.time()
#Program main()
runtime = (time.time() - start_time)

#string functions
x = "abcdefg"

#variable[ starting point : ending point : step size ]
x[::2] >> "aceg"
x[::-1] >> "gfedcba" #reverse of string
x[2:7:3] >> "cf"

#Immutability means cannot mutate. cannot change
#Strings are not mutable! (meaning you can't use indexing to change individual elements of a string)

#String replacement
x = "Ram"
x.replace("m","hul")
x>> "Rahul"

#String formating
name = 'Steven Gerrard'
number = 8
club = 'Liverpool'

"I am {0}. I play for {2}. My Kit number is {1}".format(name,number,club)
>>'I am Steven Gerrard. I play for Liverpool. My Kit number is 8'

#float formating
#{value:width.precition f}
"Answer is {x:10.4f}".format(x = 100/77)
>>'Answer is     1.2987'
#alternate method
x = 100/77
print(f"Number is {x:1.6f}")
>>Number is 1.298701

#Lists are mutable
my_list = ['x','d','g','z','xa','xx']
my_list.sort()
my_list>>['d', 'g', 'x', 'xa', 'xx', 'z']
my_list.reverse()
my_list>>['xx', 'xa', 'z', 'g', 'd', 'x']
mylist[2:5]>>['z','g','d']
[a(inclusive):b[exclusive]]

x = [1,2,3]
y = x
y[1] =  4
y>[1,4,3]
z>[1,4,3]
#This is because x doesnt store values 1,2,3. it stores the address of values 1 2 and 3. when we say y = x we are copying all address reference into y.
#Now if we change value at reference it changes for every variable pointing to that address.
#To avoid this and still copy values of x in y we do>> y = list(x) or y = x[:]

#split string by character
output_list = [x.strip() for x in testing_output.split(',')]

#Round up a number without external library
x = -(-x//1)

#Bits to bytes
no_bytes = -(-no_bits//8)

#Numpy
#List can contain elements of different types
#Numpy array can contain elements of only one type
#Numpy is used to perform element wise operations easily
a = np.array[10,20,30]
b = np.array[5,2,3]
c = [5, 5, 5]
d = [2, 2, 2]
a+b = [15, 22, 33]
c+d = [5, 5, 5, 2, 2, 2]
a/b>> [2,10,10]
c/d >> invalid

x = numpy.array(1,2,3,4,5)
#to create a bool array where all elements having value higher than 3 are True and if not false
y = x > 3
#to print values of those y elements
x[y]

#functions vs methods
type(x) >> function
x.index("abc") >> method

import numpy
>>numpy.array([1,2,3])
import numpy as np
>>np.array([1,2,3])
from numpy import array
>>array([1,2,3])

#pandas
#Accessing data from data frame
	1 Square brackets
		1 Column access >> dataframe[["Columnname1","Columnname2"]]
		2 Row access: only through slicing >> dataframe[rownumber:rownumber]
	2 loc
		1 Row access >> dataframe.loc[["Label1","Label2"]]
		2 Column access >> dataframe.loc[:,["Columnname1","Columnname2"]]
		3 Row and Column access >> dataframe.loc[["Label1","Label2"],["Columnname1","Columnname2"]]
	3 iloc
		1 Row access >> dataframe.loc[["Index1","Index2"]]
		2 Column access >> dataframe.loc[:,["Index1","Index2"]]
		3 Row and Column access >> dataframe.loc[["Index1","Index2"],["Index1","Index2"]]