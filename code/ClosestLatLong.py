#Import Libraries
from scipy import spatial
import geopy.distance
import statistics
import math
import matplotlib.pyplot as plt


#Cooridnates of all locations
Coords = [
(53.625447,	-113.507699),
(53.510946,	-113.518108),
(53.423444,	-113.600247),
(53.625496,	-113.555586),
(53.477552,	-113.352288),
(53.44941,	-113.552732),
(53.408461,	-113.478889),
(53.62808,	-113.558005),
(53.4193,	-113.568137),
(53.47755,	-113.352294),
(53.42183,	-113.623457),
(53.512882,	-113.535364),
(53.523063,	-113.476051),
(53.420579,	-113.440323),
]

# Open and read .csv file that contains the data. Heading removed
with open(r'wrfouttest.csv','r') as csv_file:
    lines = csv_file.readlines()
lines.pop(0)
#Store Lat and Long coordinates from .csv file
grid_data = []
for line in lines:
    # If cell is blank, it has made it to the end of the .csv file. Break
    if line[0]==',':
        break
    # Seperate by deliminater
    data = line.split(',')
    # Save Lat and Long to grid_dat array as an ordered pair (tuple)
    grid_data.append((float(data[1]), float(data[2])))

# Spatial.KDTree is from the scipy library for finding closest ordered pair to another
tree = spatial.KDTree(grid_data)

# Compare Latitudes
# First, obtain the latitude line that is closest to each house location (Coords) and from the data in the .csv file
# This will return both the value of distance (which has not much meaning as it is in lat/long) and index,
# which is the useful aspect. Save the index of the closest lat/long to each smart home data point.
grid_index = []
for i in range(len(Coords)):
    grid_index.append(tree.query(Coords[i])[1])
    #print(tree.query(Coords[i]))

# Obtain the lat/long of the data point closest to each smart home
nearest_grid_coords = []
for i in range(len(grid_index)):
    nearest_grid_coords.append(grid_data[grid_index[i]])
    print(grid_data[grid_index[i]])


# Compute distances in terms of meters using geopy. It takes the lat/long values of the nearest data point and smart home
# and converts that to meters.
distances = []
for i in range(len(Coords)):
    distances.append(geopy.distance.geodesic(Coords[i], nearest_grid_coords[i]).m)
#print(distances)

print('Statistical Results in Meters')
print('Mean:', statistics.mean(distances))
print('Standard Deviation:',statistics.stdev(distances))
print('Maximum Distance:',max(distances))
print('Minimum Distance:',min(distances))

# plt.hist(distances, bins=10)
# plt.title('Distances')
# plt.xlabel('Distance')
# plt.ylabel('Count')
# plt.show()

