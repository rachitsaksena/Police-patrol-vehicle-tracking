import numpy as np
import cluster
import pandas as pd
import json

cp = np.loadtxt('checkpoints.csv', delimiter=',')
r, checkpoints = cluster.geoCluster(cp, eps=1, minpts=1)
sets, regions = cluster.geoCluster(np.array(r)[:, 1:], eps=5, minpts=1)
np.set_printoptions(suppress=True)

data = {}
data["geofence"] = {}
data["geofence"]["sets"] = []
number_of_sets = len(sets)

region_group = regions.groupby('cluster')
checkpoints_group = checkpoints.groupby('cluster')

for set_number in range(number_of_sets):
    data["geofence"]["sets"].append({})
    data["geofence"]["sets"][set_number] = {
        "center" : {
            "info" : "",
            "latitude" : sets[set_number][1],
            "longitude" : sets[set_number][2],
            "radius" : sets[set_number][3]
        },
        "regions": []
    }
    regions_in_set = region_group.get_group(set_number+1)
    regions_in_set.reset_index(inplace=True, drop=True)
    # print(regions_in_set)
    for region_number, region in regions_in_set.iterrows():
        data["geofence"]["sets"][set_number]["regions"].append({})
        data["geofence"]["sets"][set_number]["regions"][region_number] = {
            "center" : {
                "info" : "",
                "latitude" : region["Latitude"],
                "longitude" : region["Longitude"],
                "radius" : region["Radius"]
            },
            "checkpoints" : []
        }
        checkpoints_in_region = checkpoints_group.get_group(region_number+1)
        checkpoints_in_region.reset_index(inplace=True, drop=True)
        # print(checkpoints_in_region)
        for checkpoint_number, checkpoint in checkpoints_in_region.iterrows():
            data["geofence"]["sets"][set_number]["regions"][region_number]["checkpoints"].append({})
            # print(*checkpoint)
            # print(checkpoint_number)
            data["geofence"]["sets"][set_number]["regions"][region_number]["checkpoints"][checkpoint_number] = {
                "info" : "",
                "latitude" : checkpoint['Latitude'],
                "longitude" : checkpoint['Longitude'],
                "radius" : checkpoint['Radius']
            }
final_data = json.dumps(data)
print(final_data)
with open("geofence_gen.json", "w") as file:
    json.dump(final_data, file)