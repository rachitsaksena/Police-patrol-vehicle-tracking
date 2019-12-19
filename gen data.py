# FIXME:
# 1) A particular set may not completely lie inside Delhi
# 2) For extremely large data generation the algorithm gets slower due to the fact that 
#    less such circles exist that do not intersect with other circles in a larger circle but lie in the same larger circle

# TODO: 
# 1) Add exception handling

import random
import json
import geopy.distance

data = {}
data["geofence"] = {}
data["geofence"]["sets"] = []
number_of_sets = random.randint(1, 2)

# Latitude and longitude extent for Delhi
min_longitude = 76.837575
max_longitude = 28.619472
min_latitude = 28.413839
max_latitude = 28.883389

sets = []
regions = []
checkpoints = []

for set_number in range(number_of_sets):
    flag = False
    set_radius = random.uniform(1, 2)
    # check if the new set is intersecting with any of the previous sets. If yes then discard co-ordinates and generate new co-ordinates till we find such a set center
    while not flag:
        set_center = (random.uniform(min_latitude, max_latitude), random.uniform(min_longitude, max_longitude))
        overlap = False
        for set in sets:
            if geopy.distance.distance(set_center, set[0]).km < (set_radius+set[1]): 
                overlap = True
                break
        if not overlap: flag = True

    sets.append((set_center, set_radius))
    data["geofence"]["sets"].append({})
    data["geofence"]["sets"][set_number] = {
        "center" : {
            "info" : "",
            "latitude" : set_center[0],
            "longitude" : set_center[1],
            "radius" : set_radius
        },
        "regions" : []
    }     
    number_of_regions = random.randint(1, 2)
    r_min_lat = set_center[0] - set_radius
    r_max_lat = set_center[0] + set_radius
    r_min_long = set_center[1] -set_radius
    r_max_long = set_center[1] + set_radius

    for region_number in range(number_of_regions):
        flag = False
        region_radius = random.uniform(0.1, 0.5)
        # check if the new region is inside its parent set and is not intersecting with any of the previous sets. 
        # If no then discard co-ordinates and generate new co-ordinates till we find such a region center
        while not flag:
            region_center = (random.uniform(r_min_lat, r_max_lat), random.uniform(r_min_long, r_max_long))
            inside = True
            overlap = False
            if geopy.distance.distance(region_center, set_center).km > (set_radius - region_radius):
                inside = False
            for region in regions:
                if geopy.distance.distance(region_center, region[0]).km < (region_radius + region[1]):
                    overlap = True
                    break
            if inside and not overlap : flag = True

        regions.append((region_center, region_radius))
        data["geofence"]["sets"][set_number]["regions"].append({})
        data["geofence"]["sets"][set_number]["regions"][region_number] = {
            "center" : {
                "info" : "",
                "latitude" : region_center[0],
                "longitude" : region_center[1],
                "radius" : region_radius
            },
            "gf" : []
        }
        number_of_checkpoints = random.randint(1, 2)
        c_min_lat = region_center[0] - region_radius
        c_max_lat = region_center[0] + region_radius
        c_min_long = region_center[1] - region_radius
        c_max_long = region_center[1] + region_radius

        for checkpoint_number in range(number_of_checkpoints):
            flag = False
            checkpoint_radius = random.uniform(0.01, 0.060)
            # check if the new checkpoint is inside its parent region and is not intersecting with any of the previous regions. 
            # If no then discard co-ordinates and generate new co-ordinates till we find such a checkpoint center
            while not flag:
                checkpoint_center = (random.uniform(c_min_lat, c_max_lat), random.uniform(c_min_long, c_max_long))
                inside = True
                overlap = False
                if geopy.distance.distance(checkpoint_center, region_center).km > (region_radius - checkpoint_radius):
                    inside = False
                for checkpoint in checkpoints:
                    if geopy.distance.distance(checkpoint_center, checkpoint[0]).km < (checkpoint_radius + checkpoint[1]):
                        overlap = True
                        break
                if inside and not overlap : flag = True

            checkpoints.append((checkpoint_center, checkpoint_radius))
            data["geofence"]["sets"][set_number]["regions"][region_number]["gf"].append({})
            data["geofence"]["sets"][set_number]["regions"][region_number]["gf"][checkpoint_number] = {
                "info" : "",
                "latitude" : checkpoint_center[0],
                "longitude" : checkpoint_center[1],
                "radius" : checkpoint_radius
            }

        # empty checkpoints list for next region
        checkpoints = []

    # empty regions list for next set
    regions = []

final_data = json.dumps(data)
with open("geofence_gen.json", "w") as file:
    json.dump(final_data, file)