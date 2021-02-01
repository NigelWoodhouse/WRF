#!/usr/bin/env python3
import netCDF4

import pandas as pd
import numpy as np
import datetime

print('Starting')
# Load file
file_name = input('Output CSV File Name: ') #Output CSV file name
load_file_name = 'wrfout_d01_2014' #wrfout file you want to read
save_file_name = file_name+'.csv'
print(load_file_name)
nc_file = load_file_name
nc = netCDF4.Dataset(nc_file, mode='r')
print('Loading data')
print('Running')

# Load variables. Variable names are determined in netCDF dictionary
lat = nc.variables['XLAT'][:]
lon = nc.variables['XLONG'][:]
time = nc.variables['XTIME']
dtime = netCDF4.num2date(time[:],time.units)

# temp = nc.variables['T2'][:] #TSK
# pressure = nc.variables['PSFC'][:]
# uWind = nc.variables['U10'][:]
# vWind = nc.variables['V10'][:]
# shortWaveUp = nc.variables['SWUPBC'][:]
# shortWaveDown = nc.variables['SWDNBC'][:]
# longWaveUp = nc.variables['LWUPBC'][:]
# longWaveDown = nc.variables['LWDNBC'][:]
# precipitationC = nc.variables['RAINC'][:]
# precipitationNC = nc.variables['RAINNC'][:]
# humidity = nc.variables['Q2'][:]
print('All variables retrieved')
# a pandas.Series designed for time series of a 2D lat,lon grid

# Convert 2D arrays to 1D
lat = lat.ravel()
lon = lon.ravel()
# temp = temp.ravel()
# pressure = pressure.ravel()
# uWind = uWind.ravel()
# vWind = vWind.ravel()
# shortWaveUp = shortWaveUp.ravel()
# shortWaveDown = shortWaveDown.ravel()
# longWaveUp = longWaveUp.ravel()
# precipitationC = precipitationC.ravel()
# precipitationNC = precipitationNC.ravel()
# longWaveDown = longWaveDown.ravel()
# humidity = humidity.ravel()

# precipitation = precipitationC + precipitationNC

# Get initial lat/ lon coordinates
start_lat = lat[0]
start_long = lon[0]

# To determine the number of data points per time interval
for i in range(1,len(lat)):
	# Looking for repeated lat/lon value. That will determine a change in time step in data
	if lat[i] == start_lat and lon[i] == start_long:
		count = i
		break
	else:
		pass
# Repeat the time variable 'count' times to align with other variables and match dimensions
dtime = np.array(list(np.repeat(dtime, count)))

print('Running')

# Data for datafram for Pandas
df={\
'Latitude':lat, 'Longitude':lon, #'Temperature [K]':temp, 
# 'Surface_Pressure [Pa]': pressure, 'X_Wind [m/s]': uWind, 'Y_wind [m/s]': vWind, 'Short_Wave_Flux_Down [W/m2]': shortWaveDown,
# 'Short_Wave_Flux_Up [W/m2]': shortWaveUp, 'Long_Wave_Flux_Down [W/m2]': longWaveDown, 'Long_Wave_Flux_Up [W/m2]': longWaveUp, 'Precipitation [mm]': precipitation, 'Humidity [kg/kg]': humidity
}


print('Data to Dictionary')
output = pd.DataFrame(data=df, index = dtime)
output.index.name = 'Time'

print('Writing')
print('Saving')

# Save file
output.to_csv(save_file_name,index=True, header=True)
nc.close()
print('Done Saving')
print('Filtering')

# Load file back
data = pd.read_csv(save_file_name)
# data = data.round(3)
data['Time'] = data['Time'].str.slice(0,16)
print('Done Filtering')
print('Saving')
	
data.to_csv(save_file_name,index=False)
print('Done')
print('########################################################')