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

spec = pd.DataFrame()

batch_dict = [
        #{'directory':'C:/Users/atlan/OneDrive/Ongoing/Subgroup/QK_IV_97/QK_IV_97TFK25', 'interval':60 },
        #{'directory':'F:/OneDrive/Ongoing/Subgroup/QK_IV_67/QK_IV_67TFK5', 'interval':60 },
        #{'directory':'F:/OneDrive/Ongoing/Subgroup/QK_IV_67/QK_IV_67TFK15', 'interval':60 },
        #{'directory':'F:/OneDrive/Ongoing/Subgroup/QK_IV_67/QK_IV_67TFK25', 'interval':60 }
        {'directory':'QK_IV_97TFK25', 'interval':60 },
        {'directory':'QK_IV_97TFK0', 'interval':60 },
        {'directory':'QK_IV_67TFK00', 'interval':60 },
        {'directory':'QK_IV_67TFK25', 'interval':60 },
        {'directory':'QK_IV_97TFK5', 'interval':60 }        
        ]

def process_spectrum(filename):
    global spec
    opus_data = read_file(filename)
    
    #print(f'Parsed fields: ' f'{list(opus_data.keys())}')
    wavenumber = opus_data.get_range("AB")
        # the "AB" data can contain more null values at the end (at least 1)
        # so the getting useful data requires slicing the array:
    spectrum = opus_data["AB"][0:len(wavenumber)-1]
    
    #print(f"Absorption spectrum range: " f"{ab_x[0]} {ab_x[-1]}")
    #print(f"Absorption elements num: " f'{len(abs)}')
    
    #print (len(spectrum))
#    print (len(wavenumber))
    Abs = []
    for i in spectrum:
        Abs.append(-math.log(i))
    
    #print("Plotting AB")
    
    df = pd.DataFrame(list(zip(wavenumber, Abs)), columns =['Wavenumber', 'Abs']) 
    
    df = df.set_index('Wavenumber')
    
    #print(df)
    
    baseline = df[(df.index >= 1590) & (df.index <= 1592) | (df.index >= 1658) & (df.index <= 1660)]
    #baseline = df[(df.index >= 1590) & (df.index <= 1592) | (df.index >= 2002) & (df.index <= 2004)]
    
    #print(baseline)
    
    baseline_value = baseline.mean()['Abs']
    
    #print(baseline_value)
    
    df['Abs'] = df['Abs'] - baseline_value
    
    #df_subset = df[(df.index >= 1590) & (df.index <=1660)]
    df_subset = df[(df.index >= 1600) & (df.index <=1705)]

    
    
    #df_subset.plot(kind='line', y='Abs',color='red')
    #plt.show()
    #print(type(df_subset),type(spec))
    spec = pd.concat([spec, df_subset],axis = 1)
    
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
        #print(1-remaining)
        
        if t > 2000:
            continue
        
        time.append(t)
        conversion.append(1-remaining)
        
        t += interval
        
    #print(spec)
    plt.plot(spec)
    plt.show()
        
    return [conversion,time]

#print (conversion)
#print (time)
        
data = []
data_export = []

cwd = os.getcwd()
#print(cwd)

for data_folder in batch_dict:
    directory = os.path.join(cwd, data_folder['directory'])
    #print(directory)
    interval = data_folder['interval']
    data.append(experiment(directory, interval))
    
for data_group in data:
    data_export.append(data_group[1])
    data_export.append(data_group[0])
    plt.plot(data_group[1], data_group[0])

plt.show()

df = pd.DataFrame(data_export)
#print(df)
df.transpose().to_csv('export.csv', index = False, header=False)









