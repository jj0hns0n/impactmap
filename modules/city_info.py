import numpy as np
from utilities import make_grid
from geodesy import Point
import sys

# Dtype for internal representation of cities
city_dtype = [('name','S10'),
              ('population',float),
              ('intensity',float),
              ('lon',float),
              ('lat',float)]

def city_info(R, B, path, eve_info):
    """List cities exposed sorted by MMI experienced

    Input
        R: Bounding box of interest
        B: MMI point values from shakemap
        path: Location of library data
        eve_info: Event info (in this case get epicentre)
    """

    # Load raw city information
    path = path+'/cities/Indonesia.txt'
    A = np.loadtxt(path, dtype={'names': ('lon', 'lat', 'pop', 'name'),
                                'formats': (float, float, float, 'S10')})


    # Mask of those cities that are inside region of interest (1D boolean array)
    mask = ((A['lon'] > R[0]) &
            (A['lon'] < R[1]) &
            (A['lat'] > R[2]) &
            (A['lat'] < R[3]))

    # Get indices of cities in region of interest (1D array of integers)
    index = np.nonzero(mask)[0]  # Get single array from tuple output

    if len(index) == 0:
        # No cities were found in region of interest.
        # Search entire database for the nearest city

        eve_lon = float(eve_info['lon'])
        eve_lat = float(eve_info['lat'])
        min_dist = sys.maxint
        for i in range(len(A)):
            start = Point(latitude=A['lat'][i], longitude=A['lon'][i])
            end = Point(latitude=eve_lat, longitude=eve_lon)
            dis = start.distance_to(end)/1000
            if dis < min_dist:
                min_dist = dis
                index = i

        # Assign MMI 0 to nearest city outside region of interest
        A = A[index]

        city = [(A['name'], A['pop'], 1, A['lon'], A['lat'])]
    else:
        # One or more cities were found in region of interest
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
    city = np.array(city, dtype=city_dtype)
    city = np.sort(city, order=['intensity', 'population'])
    city = np.flipud(city)

    return city
