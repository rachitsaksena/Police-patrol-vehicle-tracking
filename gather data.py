import numpy as np
import json

l = []

with open('geofence.json') as file:
    data = json.load(file)
    number_of_sets = len(data["geofence"]["sets"])
    for set_number in range(number_of_sets):
        number_of_regions = len(data["geofence"]["sets"][set_number]["regions"])
        for region_number in range(number_of_regions):
            number_of_checkpoints = len(data["geofence"]["sets"][set_number]["regions"][region_number]["checkpoints"])
            for checkpoint_number in range(number_of_checkpoints):
                l.append([float(data["geofence"]["sets"][set_number]["regions"][region_number]["checkpoints"][checkpoint_number]["latitude"]), float(data["geofence"]["sets"][set_number]["regions"][region_number]["checkpoints"][checkpoint_number]["longitude"]), float(data["geofence"]["sets"][set_number]["regions"][region_number]["checkpoints"][checkpoint_number]["radius"])])
dataset = np.array(l)
np.savetxt("geofences.csv", dataset, delimiter=",")