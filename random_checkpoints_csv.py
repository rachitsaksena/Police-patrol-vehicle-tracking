import numpy as np

min_longitude = 76.837575
max_longitude = 28.619472
min_latitude = 28.413839
max_latitude = 28.883389
min_radius = 0.01
max_radius = 0.06

data_size = 10

temp = np.random.rand(data_size, 1)

latitudes = temp*(max_latitude-min_latitude) + min_latitude

temp = np.random.rand(data_size, 1)

longitudes = temp*(max_longitude-min_longitude) + min_longitude

temp = np.random.rand(data_size, 1)

radius = temp*(max_radius-min_radius) + min_radius

data = np.hstack((latitudes, longitudes, radius))

np.savetxt("checkpoints_gen.csv", data, delimiter=",")