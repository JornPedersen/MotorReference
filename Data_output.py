import matplotlib.pyplot as plt

import numpy as np

from Defenitions import Column

def graphing (  motdata,
                split, 
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
            x.append(np.mean(motdata[direction,i,x_column,:].astype(float)))
            ymean.append(np.mean(motdata[direction,i,data_column1,:].astype(float)))
            ymin.append(np.amin(motdata[direction,i,data_column1,:].astype(float)))
            ymax.append(np.amax(motdata[direction,i,data_column1,:].astype(float)))
            ystddev.append(np.std(motdata[direction,i,data_column1,:].astype(float)))
            
            mean_plus3.append(np.mean(motdata[direction,i,data_column1,:].astype(float)) 
                                    + (np.std(motdata[direction,i,data_column1,:].astype(float))*3))
            
            mean_minus3.append(np.mean(motdata[direction,i,data_column1,:].astype(float)) 
                                    - (np.std(motdata[direction,i,data_column1,:].astype(float))*3))
            
            y2mean.append(np.mean(motdata[direction,i,data_column2,:].astype(float)))

        fig, ax1 = plt.subplots()
       
       
        ax1.plot(x, ymean, 'b-')
        ax1.plot(x, ymax, 'g-')
        ax1.plot(x, ymin, 'r-')
        ax1.fill_between(x, mean_plus3, mean_minus3, color = 'yellow', alpha=0.4)
        ax1.set_title   (motdata[direction,header_line,data_column1,0].replace(' 1', '')
                        +' @ '
                        + str(round(motdata[direction,split[loop],Column.voltage.value,0].astype(float),1))
                        +'V, '
                        + motdata[direction,1,8,3])
                        
        ax1.set_xlabel(motdata[direction,header_line,x_column,0].replace(' 1', ''))
        ax1.set_ylabel(motdata[direction,header_line,data_column1,0].replace(' 1', ''))
        plt.grid()

        '''
        ax2 = plt.twinx()
        ax2.plot(x, y2mean, 'b-')
        ax2.set_ylabel(mot_data[direction,header_line,data_column2,0].replace(' 1', ''))
        '''

        fig.suptitle('overordnet overskrift', fontsize = 16)

