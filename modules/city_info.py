import numpy as np
from utilities import make_grid

def city_info(R, B, path):
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

    # Clip to region of interest
    index = np.nonzero((A['lon'] > R[0]) &
                       (A['lon'] < R[1]) &
                       (A['lat'] > R[2]) &
                       (A['lat'] < R[3]))
    A = A[index]

    # Create grid of MMI values (FIXME: More explanation in here please)
    points = B[:,0:2]
    values = B[:,4]
    I = make_grid(points, values, (A['lon'], A['lat']))

    # Create city list with entries: Name, population, MMI, lon, lat

    # FIXME (Ole): Hack until ticket:2 has been addressed
    if len(A) == 0:
        # Dummy city
        intensity = [0.0]
        name = ['Kosong']
        pop = [10000]
        lon = [112.27]
        lat = [-7.530]
    else:
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







