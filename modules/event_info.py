import os
import numpy as np
def event_info(path):
    path = path + '/grid.xyz'
    file = open(path)
    line = file.readline()
    file.close()

    line = line.split(' ')

    event_info = {'mag': line[1],'lat': line[2],'lon': line[3],'month': line[4],\
                  'day': line[5],'year': line[6],'time': line[7],'time-zone': \
                  line[8],'w_bound': line[9],'s_bound': line[10],'e_bound':\
                  line[11],'n_bound': line[12]}

    

    cond = "'{if (NR!=1) print $1,$2,$5}'"
    os.system ('awk '+cond+' '+path+' > mi_tmp.txt')
    A = np.loadtxt('mi_tmp.txt')
    lon = A[:,0]
    lat = A[:,1]
    mi = A[:,2]
    
    os.system('rm mi_tmp.txt')
    return event_info,A

