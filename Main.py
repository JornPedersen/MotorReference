import os
import fnmatch
import numpy as np
import matplotlib.pyplot as plt
#from tkinter import Tk
from tkinter.filedialog import askdirectory
from tkinter import *
from enum import Enum

import re

class Direction(Enum):
    cw = 0
    ccw = 1

class Column(Enum):
    current = 0
    voltage = 1
    watts_in = 2
    efficiency = 3
    speed = 4
    torque = 5
    watts_out = 6
    cw_ccw = 7


def atoi(text):
	return int(text) if text.isdigit() else text

def natural_keys(text):
	'''
	alist.sort(key=natural_keys) sorts in human order
	http://nedbatchelder.com/blog/200712/human_sorting.html
	(See Toothy's implementation in the comments)
	'''
	return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#Create list of files in the directory matching the mask
def file_list(directory):

    lst = os.listdir(directory)
        
    lst.sort(key=natural_keys)

    return_lst = fnmatch.filter(lst, '*.mdf')       #Filter the files, only datafiles from Magtrol.

    return (return_lst)

#Read data in the files into a 2d array
def read_file(file_name):

    tmp=[]

    with open(file_name,'r') as datafile:

        for line in datafile:           #Open the file and read all the lines
            x=line.rstrip()             #Strip the \n from each line
            tmp.append(x.split('\t'))   #Split each line into a list and add it to the
                                        #2d list
        
        tmp.pop()                       #remove last entry, as there are an extra line generated.
        
        datafile.close()
        
        arr = np.array(tmp)             #Convert to 2d array
        
    return(arr)

#Create the calculated data in an 3d array, for now there are 4 different calculations made
def create_data(data_array):

                                           # Dynamically getting the size of the array.
    x = data_array.shape[0]     #lines
    y = data_array.shape[1]     #collumns
    z = data_array.shape[2]     #files (datasets)

    tmp_arr = np.zeros((z))              
    result_arr = np.zeros((4,x,y-1))         #First axis is only of size 4, to reflect that there are 4 different 
                                            #calculations made on the data array
    
    #This is nested loops, could be changed to slicing to make it simpler
    for ax2 in range(0,y-1):               #Skip last collumn, as it holds the direction inforation
        for ax1 in range(1,x):             #Skip first row, as it holds the headers
            for ax0 in range(0,z):
                tmp_arr[ax0] = data_array[ax1,ax2,ax0]
            result_arr[0, ax1, ax2] = np.mean(tmp_arr)
            result_arr[1, ax1, ax2] = np.amin(tmp_arr)
            result_arr[2, ax1, ax2] = np.amax(tmp_arr)
            result_arr[3, ax1, ax2] = np.std(tmp_arr)


    return(result_arr)


#Make a list on where to split the big data array
def split_id(data):

    split_arr = []
    old_data = data[0]
    split_arr.append(1)


    for i in range(0, (data.size)):
        if old_data - data[i] > 1:
            split_arr.append(i+1)
            old_data = data[i]
        else:
            old_data = data[i]
    
    split_arr.append(data.size + 1)

    return(split_arr)


def read_data(in_data) :

    out_cw = np.array([])
    out_ccw = np.array([])

    files = file_list(in_data)                 #Create a list of files in the actual directory

    for name in files: 
        
        tmp = read_file(in_data + name)        #Create the data list from the choosen files
        
        if tmp[5][8]=='CW' :                    #Simple check, only one cell is checked.
            if out_cw.size == 0 :                   #To Do: check all data-lines, as there can be faulty entries.
                out_cw = tmp
            else :
                out_cw = np.dstack((tmp, out_cw))
        else :
            if out_ccw.size == 0 :
                out_ccw = tmp
            else :
                out_ccw = np.dstack((tmp, out_ccw))

                                                # 3d array, content:
                                                # 1. dimension is line
                                                # 2. dimension is collumn
                                                # 3. dimension is dataset(file)
    
    if out_cw.size == 0 or out_ccw.size == 0 :

        if out_cw.size == 0 :
            out_cw = np.zeros_like(out_ccw)
        
        if out_ccw.size == 0 :
            out_ccw = np.zeros_like(out_cw)

    stakket = np.stack([out_cw,out_ccw])

    return(stakket)


def graphing (  split, 
                direction,
                data_column1,
                data_column2,
                header_line,
                x_column
                ) :

    for loop in range (0,(len(split)-1)) :
        x=[]
        ymean=[]
        ymin=[]
        ymax=[]
        ystddev=[]
        mean_plus3 = []
        mean_minus3 = []
        y2mean=[]
        for i in range(split[loop],split[loop+1]):
            x.append(np.mean(mot_data[direction,i,x_column,:].astype(float)))
            ymean.append(np.mean(mot_data[direction,i,data_column1,:].astype(float)))
            ymin.append(np.amin(mot_data[direction,i,data_column1,:].astype(float)))
            ymax.append(np.amax(mot_data[direction,i,data_column1,:].astype(float)))
            ystddev.append(np.std(mot_data[direction,i,data_column1,:].astype(float)))
            
            mean_plus3.append(np.mean(mot_data[direction,i,data_column1,:].astype(float)) 
                                    + (np.std(mot_data[direction,i,data_column1,:].astype(float))*3))
            
            mean_minus3.append(np.mean(mot_data[direction,i,data_column1,:].astype(float)) 
                                    - (np.std(mot_data[direction,i,data_column1,:].astype(float))*3))
            
            y2mean.append(np.mean(mot_data[direction,i,data_column2,:].astype(float)))

        fig, ax1 = plt.subplots()
       
       
        ax1.plot(x, ymean, 'b-')
        ax1.plot(x, ymax, 'g-')
        ax1.plot(x, ymin, 'r-')
        ax1.fill_between(x, mean_plus3, mean_minus3, color = 'yellow', alpha=0.4)
        ax1.set_title   (mot_data[direction,header_line,data_column1,0].replace(' 1', '')
                        +' @ '
                        + str(round(mot_data[direction,split[loop],Column.voltage.value,0].astype(float),1))
                        +'V, '
                        + mot_data[direction,1,8,3])
                        
        ax1.set_xlabel(mot_data[direction,header_line,x_column,0].replace(' 1', ''))
        ax1.set_ylabel(mot_data[direction,header_line,data_column1,0].replace(' 1', ''))
        plt.grid()

        '''
        ax2 = plt.twinx()
        ax2.plot(x, y2mean, 'b-')
        ax2.set_ylabel(mot_data[direction,header_line,data_column2,0].replace(' 1', ''))
        '''

        fig.suptitle('overordnet overskrift', fontsize = 16)


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

print ('stakket shape:',mot_data.shape)
print('dim 0 :',mot_data[Direction.cw.value,1,8,0])
print('dim 1 :',mot_data[Direction.ccw.value,1,8,0])


if mot_data[0,1,8,0] != '' :
    splitlist=split_id(mot_data[Direction.cw.value,
                                1:,
                                Column.voltage.value,
                                0].astype(float))
    print(splitlist)
    graphing(   splitlist, 
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
    print(splitlist)
 
    print (len(splitlist))
    graphing(   splitlist, 
                Direction.ccw.value,
                Column.efficiency.value,
                Column.current.value,
                0,
                Column.torque.value)

plt.show()
	