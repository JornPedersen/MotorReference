# import os
# import fnmatch
# import numpy as np

#from tkinter import Tk
from tkinter.filedialog import askdirectory
from tkinter import *

from Defenitions import Direction,Column

from Data_input import *
from Data_handling import *
from Data_output import *



    #plt.savefig('first.png')
    #plt.savefig('first.pdf')


#Main program


data_dir = askdirectory(title='Select Folder') + '/' # shows dialog box and return the path
#print(data_dir)  

root=Tk()
def retrieve_input():
    inputValue=textBox.get("1.0","end-1c")
    print(inputValue)

textBox=Text(root, height=2, width=10)
textBox.pack()
buttonCommit=Button(root, height=1, width=10, text="Commit", 
                    command=lambda: retrieve_input())
#command=lambda: retrieve_input() >>> just means do this when i press the button
buttonCommit.pack()

root.mainloop()

mot_data = read_data(data_dir)

# print ('stakket shape:',mot_data.shape)
# print('dim 0 :',mot_data[Direction.cw.value,1,8,0])
# print('dim 1 :',mot_data[Direction.ccw.value,1,8,0])


if mot_data[0,1,8,0] != '' :
    splitlist=split_id(mot_data[Direction.cw.value,
                                1:,
                                Column.voltage.value,
                                0].astype(float))
#    print(splitlist)
    graphing(   mot_data,
                splitlist, 
                Direction.cw.value,
                Column.efficiency.value,
                Column.current.value,
                0,
                Column.torque.value)

if mot_data[1,1,8,0] != '' :
    splitlist=split_id(mot_data[Direction.ccw.value,
                                1:,
                                Column.voltage.value,
                                0].astype(float))
#    print(splitlist)
 
#    print (len(splitlist))
    graphing(   mot_data,
                splitlist, 
                Direction.ccw.value,
                Column.efficiency.value,
                Column.current.value,
                0,
                Column.torque.value)

plt.show()
	