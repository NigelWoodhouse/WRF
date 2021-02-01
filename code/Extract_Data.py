# Used to extract the data and variables from netcdf/wrfout files and put them in csv files.
# Refer to this video https://www.youtube.com/watch?v=hrm5RmsVXo0
from netCDF4 import Dataset
import numpy as np
from datetime import datetime
from datetime import timedelta
import pandas as pd
import math

data = Dataset('wrfout_file', 'r') # Load the netCDF4 wrfout file.
# print(data.variables.keys()) # Prints a list of the avaliable variables from the file

# All the Coordinates that you are interested in, which loops through. (Latitude, Longitude, Name -> for saving)
Coords = [ 
(53.62594,  -113.506195,    'egauge18356'), 
(53.507202, -113.52429,     'egauge18366'), 
(53.4208,   -113.59668,     'egauge18360'), 
(53.625916, -113.56079,     'egauge18357'), 
(53.474754, -113.36105,     'egauge18369'), 
(53.453213, -113.5605,      'egauge18359'), 
(53.41006,  -113.46988,     'egauge18371'), 
(53.625916, -113.56079,     'egauge18358'), 
(53.420834, -113.560455,    'egauge18374'), 
(53.474754, -113.36105,     'egauge18367'), 
(53.420788, -113.61478,     'egauge18364'), 
(53.517982, -113.54245,     'egauge18361'), 
(53.517994, -113.46985,     'egauge18365'), 
(53.42084,  -113.433655,    'egauge18355'), 
(53.453213, -113.5605,      'egauge18372'),
]

# Date range for data extraction

start_offset =  0     
# In number of timesteps, time to offset extraction by:
# Set to 0 if you want to begin extracting from the start of the file.
# If you want to start extracting after 1 day, with a 5 min timestep, set start_offset to 288.

end_offset =    0     
# In number of timesteps, time to offset extraction by:
# Set to 0 if you want to stop extracting at the end of the file.
# If you want 1 day of data, with a 5 min timestep, set end_offset to 288.

latitude = data.variables['XLAT'][0,:,0] # Get all of the Latitude points
longitude = data.variables['XLONG'][0,0,:] # Get all of the Longitude points
initial_time_index = int(data.variables['XTIME'][0]) # Get the first time index. 0 is default unless another file was created during sumuation. else, frames_per_outfile multiple
timestep = round((data.variables['XTIME'][1] - initial_time_index),0) # timestep in simulation -> assuming natural number of minutes
num_timesteps = len(data.variables['XTIME'][:]) # number of timesteps in file

# For all points of interest
for Coord in Coords:
    # GET CLOSEST POINT
    sq_diff_latitude = (latitude - Coord[0])**2 # Find the closest latitude location
    sq_diff_longitude = (longitude - Coord[1])**2 # Find the closest longitude location

    min_index_lat = sq_diff_latitude.argmin() # Get the index for the closest latitude location
    min_index_lon = sq_diff_longitude.argmin() # Get the index for the closest longitude location

    # print(min_index_lat,min_index_lon) # Print those indicies to terminal

    # TIME EXTRACT
    #For figuring out datetime for index in csv file
    start_date = data.variables['XTIME'].units[14:24] # Get the beginning time of simulation (does not mean start of this file loaded; that is accounted for later)
    start_date = datetime.strptime(start_date, '%Y-%m-%d') # Convert to datetime

    # When to start, adjusted by start_offset
    start_date = start_date + timedelta(minutes=initial_time_index) + timedelta(minutes=start_offset*timestep) # If starting at beginning of file

    if end_offset == 0: # Get data to end of file
        end_date = start_date + timedelta(minutes=(num_timesteps-start_offset)*timestep)
    else: # Get data up to point specified by end_offset
        end_date = start_date + timedelta(minutes=(end_offset)*timestep)
    
    # Date range for pandas dataframe
    date_range = pd.date_range(start = start_date, end = end_date-timedelta(minutes=timestep), freq = str(timestep)+"min", name="Time [UTC]").strftime('%Y-%m-%d %H:%M')

    # Place the variables you want to extract here. Be aware that some variables have an extra height dimension. You can check this by print(data.variables['VAR'])
    # Coordinates are [Time, Height (if applicable), Latitude, Longitude]
    # Additional lines should follow the same format. Uncomment line 11 [print(data.variables.keys())] to see the avaliable key pairs. 
    # Additional reference near the bottom: https://www2.mmm.ucar.edu/wrf/users/docs/user_guide_v4/v4.0/users_guide_chap5.html
    # Additional note: Total precipitation equals RAINC + RAINNC
    temp = data.variables['T2']
    X_Wind = data.variables['U10']
    Y_Wind = data.variables['V10']

    # Creating the pandas dataframe. Place titles of variables here.
    df = pd.DataFrame(0, columns = ['Temperature [K]', 'X_Wind [m/s]', 'Y_Wind [m/s]'], index = date_range)

    # Extracting the data for each time step, for each variable. Add extra lines for each variables with the same format.
    for time_index in range(len(date_range)):
        df.iloc[time_index,0] = temp[time_index + start_offset, min_index_lat, min_index_lon]
        df.iloc[time_index,1] = X_Wind[time_index + start_offset, min_index_lat, min_index_lon]
        df.iloc[time_index,2] = Y_Wind[time_index + start_offset, min_index_lat, min_index_lon]

    # Save to csv file.
    print('Saving ' +  Coord[2]+'_'+str(start_date)[0:10]+'.csv')
    df.to_csv(Coord[2]+'_'+str(start_date)[0:10]+'.csv')