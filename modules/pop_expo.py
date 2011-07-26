import pickle
import numpy as np
#from utilities import make_grid
from scipy.interpolate import griddata

def pop_expo(event_info,A,path):
    pkl_file = open(path+'/population/landscan2008_binary.pkl','r')
    ls = pickle.load(pkl_file)
    ls = np.flipud(ls)
    pkl_file.close()
    pkl_file = open(path+'/population/landscan2008_info.pkl','r')
    ls_info = pickle.load(pkl_file)
    pkl_file.close()

    R = np.zeros(4, dtype = float)
    R[0] = np.maximum(float(event_info['w_bound']),ls_info['w_bound'])
    R[1] = np.minimum(float(event_info['e_bound']),ls_info['e_bound'])
    R[2] = np.maximum(float(event_info['s_bound']),ls_info['s_bound'])
    R[3] = np.minimum(float(event_info['n_bound']),ls_info['n_bound'])

    # Check that population and event data overlap
    msg = ('Population data and event data did not overlap:\n'
           'Event data: %s\n'
           'Population: %s' % (str(event_info), str(ls_info)))
    assert R[0] < R[1] and R[2] < R[3], msg

    dl = ls_info['step']
    col_low = np.abs(R[0]-ls_info['w_bound'])/dl
    col_low = np.ceil(col_low);
    col_high = np.abs(R[1]-ls_info['w_bound'])/dl
    col_high = np.floor(col_high);
    row_low = np.abs(R[2]-ls_info['s_bound'])/dl
    row_low = np.ceil(row_low);
    row_high = np.abs(R[3]-ls_info['s_bound'])/dl
    row_high = np.floor(row_high);

    x_min = col_low*dl+ls_info['w_bound']
    x_max = col_high*dl+ls_info['w_bound']
    y_min = row_low*dl+ls_info['s_bound']
    y_max = row_high*dl+ls_info['s_bound']

    Nx = col_high - col_low
    Ny = row_high - row_low
    x, dx = np.linspace(x_min, x_max, Nx, endpoint=False, retstep=True)
    y, dy = np.linspace(y_min, y_max, Ny, endpoint=False, retstep=True)


    msg = ('Step size of landscan subgrid in the x direction inconsistent '
           'with original landscape grid. Got %f expected %f' % (dx, dl))
    assert np.allclose(dx, dl, rtol=1.0e-12, atol=1.0e-12), msg


    msg = ('Step size of landscan subgrid in the y direction inconsistent '
           'with original landscape grid. Got %f expected %f' % (dy, dl))
    assert np.allclose(dy, dl, rtol=1.0e-12, atol=1.0e-12), msg



    [X,Y] = np.meshgrid(x,y)

    Z_pop = ls[row_low:row_high, col_low:col_high]
    Z_pop[Z_pop == -9999] = np.NaN


    # Get MMI point data
    points = A[:,0:2]
    values = A[:,4]
    Z_I = griddata(points, values, (X,Y), method='cubic')

    #print 'len', len(X),len(Z_I)

    I = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    pop_expo = np.zeros(9, dtype='float')
    k = -1
    for i in I:
        index = np.nonzero((Z_I >= i - 0.5) & (Z_I < i + 0.5))
        k = k+1

        # Temporary debug print statements
        #print 'k', k, 'i', i
        #print 'index', index
        #print 'sum', np.nansum(Z_pop[index])
        # Round affected population to the nearest 1000
        x = np.nansum(Z_pop[index])
        pop_expo[k] = round(x/1000)*1000

    pop_expo [np.isnan(pop_expo)] = 0
    I = ['II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
    pop_expo = dict(zip(I,pop_expo))

    return pop_expo, R





