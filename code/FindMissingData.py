import os
import pandas as pd
from datetime import datetime
import numpy as np

# Used for cleaning up some erroneous data and if there are any discontinuities in the time-series data

# The name of the firectory that the concatonated CSV file exists in has the same name as its directory. You may need to make
# adjustments based upon the way you have organized your files and directories.

# Concatonated files + directory names
Directory = [ 
'egauge18356',
'egauge18366',
'egauge18360',
'egauge18357',
'egauge18369',
'egauge18359',
'egauge18371',
'egauge18358',
'egauge18374',
'egauge18367',
'egauge18364',
'egauge18361',
'egauge18365',
'egauge18355',
'egauge18372',
]

# CLEANING DATA
for file in Directory:
    df = pd.read_csv(r'LOCATION_WHERE_THE_FILE_IS\\'+file+'\\'+file+'.csv') # Change based upon where you saved the data
    df = df.drop_duplicates(subset=['Time (UTC)']) # remove duplicates
    print(file)

    # For my work, at the beginning of a simulation, all the radiation values were 0. In the concatonated CSV file, I could therefore tell where 
    # One CSV file ended and another began based on this line of zeros -> kind of a hacky way to go about it. So I set those 0 values to null, then interpolate
    # in an attempt to smooth the discontinuities. You may want to figure out a better way to find these breaks. If your csv files start on a daily basis,
    # checking times may be a better option.
    df.loc[df['Long_Wave_Flux_Down [W/m2]'] == 0,  'Short_Wave_Flux_Down [W/m2]'] = np.nan
    df.loc[df['Long_Wave_Flux_Down [W/m2]'] == 0,  'Short_Wave_Flux_Up [W/m2]'] = np.nan
    df.loc[df['Long_Wave_Flux_Down [W/m2]'] == 0,  'Long_Wave_Flux_Down [W/m2]'] = np.nan
    df.loc[df['Long_Wave_Flux_Up [W/m2]'] == 0,  'Long_Wave_Flux_Up [W/m2]'] = np.nan
    df = df.interpolate() # interpolate null data
    df = df.fillna(method='bfill') # For the first row, as you cannot interpolate. Just backfill.
    df.to_csv(r'LOCATION_WHERE_THE_FILE_IS\\'+file+'\\'+file+'.csv', index = False) # Overwrite file.

# TESTING MISSING DATA POINTS, like if you missed a day of simulation, for example.
print('testing')
# You should only need to check one file for missing data, as all files are generated in the same manner. If this file is missing data, they all are.
df = pd.read_csv(r'LOCATION_WHERE_THE_FILE_IS\egauge18356\egauge18356.csv')
fmt = '%Y-%m-%d %H:%M' # datetime format
for index, row in df.iterrows(): # iterate through all rows
    Time1 = (row['Time (UTC)']) # Checking the time column
    Time1 = datetime.strptime(Time1, fmt) # Get in the form of datetime for comparison
    if index == 0: # First index
        Time2 = Time1 # Set times
    delta = (Time1 - Time2).total_seconds() / 60.0 # Difference between two consecutive times
    if delta != 5 and index != 0: # The change in time, in my case, should be 5 minutes. Adjust accordingly. Also, ignore the first entry.
        print(index, Time2, Time1)     # If there is a discontinuity in the time series, it will print the time and index in from the .csv file, which you can check afterwards in excel.
                                # If there is, you will have to go about simulating that part of the data, extracting data, concatenating, and running this again. 
    Time2 = Time1 # Reset for next row