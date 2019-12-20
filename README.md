# Police-patrol-vehicle-tracking
For Clustering:
1. gen data.py creates a randomized geo tree and saves it as geofence_gen.json
2. gather data.py extracts all checkpoints from a geotree json
3. mydbscan.py and cluster.py are for internal use and gen json.py is the final file that reads input from checkpoints.csv and outputs the geotree in gefences_gen.json file
4. random_checkpoints_csv.py generates data for random checkpoints and saves it as checkpoint_gen.csv