import os
import numpy as np


def event_info(shakedata_dir, event_name):
    """Read shakemap event information and return it as an Array

    Input
        shakedata_dir
        event_name

    Output
        event_info: Dictionary of earthquake event data
        A: Nx8 array with the columns of grid.xyz
    """

    path = os.path.join(shakedata_dir, event_name, 'output', 'grid.xyz')
    fid = open(path)
    line = fid.readline()
    fid.close()

    fields = line.split(' ')

    event_info = {'mag': fields[1],
                  'lat': fields[2],
                  'lon': fields[3],
                  'month': fields[4],
                  'day': fields[5],
                  'year': fields[6],
                  'time': fields[7],
                  'time-zone': fields[8],
                  'w_bound': fields[9],
                  's_bound': fields[10],
                  'e_bound': fields[11],
                  'n_bound': fields[12]}

    A = np.loadtxt(path, dtype=float, skiprows=1)
    return event_info, A

