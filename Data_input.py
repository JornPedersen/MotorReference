
from tkinter.filedialog import askdirectory
from tkinter import *

import numpy as np

import os

import fnmatch

import re

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

def DataInput() :
    
   
    
    return()