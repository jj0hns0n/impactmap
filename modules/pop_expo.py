import pickle
import numpy as np
from utilities import make_grid


def pop_expo(event_info,A,path):
    pkl_file = open(path+'/population/landscan_binary.pkl','r')
    ls = pickle.load(pkl_file)
    ls = np.flipud(ls)
    pkl_file.close()
    pkl_file = open(path+'/population/landscan_info.pkl','r')
    ls_info = pickle.load(pkl_file)
    pkl_file.close()

    R = np.zeros(4,dtype = float)
    R[0] = np.maximum(float(event_info['w_bound']),ls_info['w_bound'])
    R[1] = np.minimum(float(event_info['e_bound']),ls_info['e_bound'])
    R[2] = np.maximum(float(event_info['s_bound']),ls_info['s_bound'])
    R[3] = np.minimum(float(event_info['n_bound']),ls_info['n_bound'])

    dl = ls_info['step']
    col_low = np.abs(R[0]-ls_info['w_bound'])/dl
    col_low = np.ceil(col_low);
    col_high = np.abs(R[1]-ls_info['w_bound'])/dl
    col_high = np.floor(col_high);
    row_low = np.abs(R[2]-ls_info['s_bound'])/dl
    row_low = np.ceil(row_low);
    row_high = np.abs(R[3]-ls_info['s_bound'])/dl
    row_high = np.floor(row_high);

    x_min = col_low*dl+ls_info['w_bound'];
    x_max = col_high*dl+ls_info['w_bound'];
    y_min = row_low*dl+ls_info['s_bound'];
    y_max = row_high*dl+ls_info['s_bound'];

    x = np.arange(x_min,x_max+dl,dl)
    y = np.arange(y_min,y_max+dl,dl)
    [X,Y] = np.meshgrid(x,y)
    Z_pop = ls[row_low:row_high+1][:,col_low:col_high+1]
    Z_pop[Z_pop==-9999]= np.NaN

    points = A[:,0:2]
    values = A[:,2]
    Z_I = make_grid(points, values, (X, Y))


    I = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    pop_expo = np.zeros(9,dtype = 'float')
    k = -1
    for i in I:
        index = np.nonzero((Z_I>=i-0.5)&(Z_I<i+0.5))
        k = k+1
        pop_expo[k] =  np.nansum(Z_pop[index])

    pop_expo [ np.isnan(pop_expo)] = 0
    I = ['II','III','IV','V','VI','VII','VIII','IX','X']
    pop_expo = dict(zip(I,pop_expo))
    return pop_expo,R





