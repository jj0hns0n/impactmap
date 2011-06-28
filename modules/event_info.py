import os
import numpy as np


def event_info(shakedata_dir, event_name):
    """Read shakemap event information and return it as an Array

    Input
        shakedata_dir
        event_name

    Output
        event_info: Dictionary of earthquake event data
        A: Nx5 array
    """

    path = os.path.join(shakedata_dir, event_name, 'output', 'grid.xyz')
    fid = open(path)
    line = fid.readline()
    fid.close()

    line = line.split(' ')

    event_info = {'mag': line[1],
                  'lat': line[2],
                  'lon': line[3],
                  'month': line[4],
                  'day': line[5],
                  'year': line[6],
                  'time': line[7],
                  'time-zone': line[8],
                  'w_bound': line[9],
                  's_bound': line[10],
                  'e_bound': line[11],
                  'n_bound': line[12]}

    A = np.loadtxt(path, dtype=float, skiprows=1)
    return event_info, A

