# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 20:37:50 2020

@author: atlan
"""
import math
import matplotlib.pyplot as plt
from brukeropusreader import read_file
import pandas as pd
import os

batch_dict = [
        {'directory':'F:/OneDrive/Ongoing/Subgroup/201002/172a/TFK0', 'interval':30 },
        {'directory':'F:/OneDrive/Ongoing/Subgroup/201002/172a/TFK25', 'interval':30 },
        ]

def process_spectrum(filename):
    opus_data = read_file(filename)
    
    #print(f'Parsed fields: ' f'{list(opus_data.keys())}')
    wavenumber = opus_data.get_range("AB")
        # the "AB" data can contain more null values at the end (at least 1)
        # so the getting useful data requires slicing the array:
    spectrum = opus_data["AB"][0:len(wavenumber)]
    
    #print(f"Absorption spectrum range: " f"{ab_x[0]} {ab_x[-1]}")
    #print(f"Absorption elements num: " f'{len(abs)}')
    
#    print (len(spectrum))
#    print (len(wavenumber))
    Abs = []
    for i in spectrum:
        Abs.append(-math.log(i))
    
    #print("Plotting AB")
    
    df = pd.DataFrame(list(zip(wavenumber, Abs)), columns =['Wavenumber', 'Abs']) 
    
#    print(df)
    
    df = df.set_index('Wavenumber')
    #df_subset = df[(df.index >= 1590) & (df.index <= 1660)]
    #df_subset.plot(kind='line', y='Abs',color='red')
    #plt.show()
    
    aromatic = df[(df.index >= 1600) & (df.index <= 1620)].max()
    vinyl = df[(df.index >= 1630) & (df.index <= 1645)].max()
    ratio = vinyl/aromatic
    #print(aromatic,vinyl)
    #print (ratio.get(key = 'Abs'))
    return(ratio.get(key = 'Abs'))



def experiment(directory, interval):
    conversion = []
    time = []
    t = 0
    
    for filename in os.listdir(directory):
        print(filename)
        file = (os.path.join(directory, filename))
        ratio = process_spectrum(file)
        #print(ratio)
        if t == 0:
            ratio_0 = ratio
            
        remaining = ratio/ratio_0
        print(1-remaining)
        
        time.append(t)
        conversion.append(1-remaining)
        
        t += interval
        
    return [conversion,time]

#print (conversion)
#print (time)
        
data = []

for data_folder in batch_dict:
    directory = data_folder['directory']
    interval = data_folder['interval']
    data.append(experiment(directory, interval))
    
for data_group in data:
    plt.plot(data_group[1], data_group[0])

plt.show()











