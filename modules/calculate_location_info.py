"""Calculate distance from earthquake to most affected city
"""

def calculate_distance(p1, p2):
    """Calculate distance between to locations

    Input:
        p1: (lon, lat) pair in decimal degrees of first point
        p2: (lon, lat) pair in decimal degrees of last point
    """

    # FIXME (Ole): Small wrapper until ticket #7 is done
    from points2distance import points2distance

    start = ((p1[0], 0, 0),  (p1[0], 0, 0))
    end = ((p2[0], 0, 0),  (p2[0], 0, 0))
    return points2distance(start, end)

def calculate_location_info(event_info, city_info):
    """Calculate distance from earthquake to most affected city

    Input
        event_info: Information about earthquake
        city_info: List of cities sorted by intensity

    Note all information is passed in to allow future modifications such
    as options for calculating
    * distance to nearest city
    * distance to most affected city
    * distance to biggest city
    * etc
    """

    # Get location of earthquake
    lat = float(event_info['lat'])  # FIXME: Should store these as floats
    lon = float(event_info['lon'])

    # Select city (in this case, take the most affected)
    city = city_info[0]

    # Get location and name of selected city
    name = city[0]
    city_lat = city[4]
    city_lon = city[3]

    # Compute distance
    d = calculate_distance((lon, lat), (city_lon, city_lat))

    # Create string and update event_info
    s = '%ikm dari %s' % (d, name)
    event_info['location_string'] = s


