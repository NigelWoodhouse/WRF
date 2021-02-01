#!/usr/bin/env python3
import glob
import pandas as pd
import os
import datetime as dt
# Concatonate your csv output files.

# File/Directory names that you want to concatonate.
# I saved my outputs to different directories with similar names organized by their location/eguage#####.
# For Example: eguage18356 > eguage18356_01-01-01_00:00:00.csv
# Additionally, I organized files by city, as I was working on multiple locations at a time.
# Your file management may be different, so make the proper ammendments to directories.
Directories = [
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
'egauge18372'
]
# Looping through all files in all specified directories above, keeping in mind directories and files have similar naming.
for files in Directories:
    li = [] # Ensure that list of dataframes is clear upon iterations
    print('Starting')
    os.chdir(r'/home/YOUR_ACCOUNT/scratch/Results/Edmonton/CSVFiles/'+files+'/') # Operating directory, done on cluster
    all_files = glob.glob(r'/home/YOUR_ACCOUNT/scratch/Results/Edmonton/CSVFiles/'+files+'/' + "*"+files+"*") # Getting all of the files. Using * with glob acts as a whidcard.

    for filename in all_files: # Loading up the .csv files into data frames, and appending those dataframes to the list
        df = pd.read_csv(filename, index_col=None, header=0) # Read .csv files
        li.append(df) # Append all .csv files
    os.chdir(r'/home/YOUR_ACCOUNT/scratch/Results/Edmonton/ConcatCSVFiles/'+files+'/') # Change directory to where I am saving the results

    df = pd.concat(li, axis=0, ignore_index=True) # Concat all of the dataframes together
    df['Time (UTC)'] = pd.to_datetime(df['Time (UTC)']) # Make time column datetime format rather than string, for organizing
    df = df.sort_values(by='Time (UTC)') # Organize data
    df = df.round(3) # 3 Significant digits
    df['Time (UTC)'] = df['Time (UTC)'].dt.strftime("%Y-%m-%d %H:%M") # Return datetime to string for .csv file
    df.to_csv(files+'.csv', index = False) # Save to .csv
    df = df.empty # Ensure that dataframe is clear for next interation
    print('Done', files)