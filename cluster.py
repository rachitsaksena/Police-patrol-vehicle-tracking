import mydbscan
import numpy as np
import geopy.distance
import pandas as pd

def geoCluster(data, eps=1, minpts=1):
    """Data should have 3 columns: Latitiude, Longitude, Radius (in that order)"""
    labels = mydbscan.MyDBSCAN(data, eps, minpts)

    clusters = pd.DataFrame(np.hstack((data, np.array(labels).reshape(-1,1))), columns=['Latitude', 'Longitude', 'Radius', 'cluster'])

    groups = clusters.groupby('cluster')
    geofences = []
    for label in set(labels):
        d = np.array(groups.get_group(label))
        centroid = (np.mean(d[:, 0]), np.mean(d[:, 1]))
        max_distance = 0
        for row in d:
            distance = geopy.distance.distance(centroid, (row[0], row[1])).km
            if distance>max_distance: max_distance = distance
        if max_distance>=eps:
            geofences.append([label, centroid[0], centroid[1], max_distance+0.1])
        else:
            geofences.append([label, centroid[0], centroid[1], eps+0.1])
    return geofences, clusters

# data = np.loadtxt('geofences.csv', delimiter=',')
# geofences = np.array(geocluster(data, eps=1, minpts=1))
