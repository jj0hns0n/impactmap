import numpy as np
from utilities import make_grid

def city_info(R,B,path):
    path = path+'/cities/Indonesia.txt'
    A = np.loadtxt(path,dtype={'names': ('lon','lat','pop','name'),\
                                      'formats': (float,float,float,'S10')})

    index = np.nonzero((A['lon']>R[0])& (A['lon']<R[1]) & (A['lat']>R[2]) & \
                       (A['lat']<R[3]))


    A = A[index]
    print np.shape(A)
    I = make_grid(B[:, 0], B[:, 1], B[:, 2], A['lon'], A['lat'])

    city = zip(A['name'].tolist(),A['pop'].tolist(),I.tolist(),A['lon'].tolist(),A['lat'].tolist())


    dtype = [('name','S10'),('population',float),('intensity',float),('lon',float),('lat',float)]
    city = np.array(city,dtype=dtype)
    city = np.sort(city,order=['intensity','population'])

    city = np.flipud(city)
    return city







