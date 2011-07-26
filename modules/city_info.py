import numpy as np
from utilities import make_grid
import points2distance

def city_info(R, B, path, eve_info):
    """List cities exposed sorted by MMI experienced

    Input
        R: Bounding box of interest
        B: ??? MMI point values.....
        path: Location of library data
    """

    # Load raw city information
    path = path+'/cities/Indonesia.txt'
    A = np.loadtxt(path, dtype={'names': ('lon', 'lat', 'pop', 'name'),
                                'formats': (float, float, float, 'S10')})

    
    print R[0],R[1],R[2],R[3]
    # Clip to region of interest
    index = np.nonzero((A['lon'] > R[0]) &
                       (A['lon'] < R[1]) &
                       (A['lat'] > R[2]) &
                       (A['lat'] < R[3]))
    
    
    if index:
       eve_lon = float(eve_info['lon'])
       eve_lat = float(eve_info['lat'])
       dist_dum = 1e08
       print dist_dum
       for i in range(len(A)):
           start = ((A['lon'][i],0,0),(A['lat'][i],0,0))
           end = ((eve_lon,0,0),(eve_lat,0,0))
           dis = points2distance.points2distance(start,end)
           if dis<dist_dum:
              index =i
         
       A = A[index]
       print A
       city = dict([('name',A['name']),('population',A['pop']),('intensity',0),('lon',A['lon']),('lat',A['lat'])])
       city = np.array(city)
       print 'length=', city, len(city)
    else:
       A = A[index]
    # Create grid of MMI values (FIXME: More explanation in here please)
       points = B[:,0:2]
       values = B[:,4]
       I = make_grid(points, values, (A['lon'], A['lat']))

    # Create city list with entries: Name, population, MMI, lon, lat
       intensity = I.tolist()
       name = A['name'].tolist()
       pop = A['pop'].tolist()
       lon = A['lon'].tolist()
       lat = A['lat'].tolist()
       city = zip(name, pop, intensity, lon, lat)

    # Convert to array and sort by intensity
    # (and population if intensity is the same)
       dtype = [('name','S10'),
             ('population',float),
             ('intensity',float),
             ('lon',float),
             ('lat',float)]
       city = np.array(city, dtype=dtype)
       city = np.sort(city, order=['intensity', 'population'])
       city = np.flipud(city)

    return city







