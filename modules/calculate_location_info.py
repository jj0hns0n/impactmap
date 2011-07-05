"""Calculate distance from earthquake to most affected city
"""

from geodesy import Point

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

    # Get location of earthquake  FIXME: Should store these as floats
    earthquake_location = Point(float(event_info['lat']),
                                float(event_info['lon']))

    # Select city (in this case, take the most affected)
    city = city_info[0]

    # Get location and name of selected city
    city_name = city[0]
    city_location = Point(city[4], city[3])

    # Compute distance [m] and bearing [deg from city]
    d = city_location.distance_to(earthquake_location)
    b = city_location.bearing_to(earthquake_location)

    # Create string and update event_info
    if 5 <= b < 85:
        direction = 'Timur Laut'  # North East
    elif 85 <= b < 95:
        direction = 'Timur'       # East
    elif 95 <= b < 175:
        direction = 'Tenggara'    # South East
    elif 175 <= b < 185:
        direction = 'Selatan'      # South
    elif 185 <= b < 265:
        direction = 'Barat Daya'  # South West
    elif 265 <= b < 275:
        direction = 'Barat'       # West
    elif 275 <= b < 355:
        direction = 'Barat Laut'  # North West
    else:
        direction = 'Utara'       # North

    s = 'Berjarak %i km, %i$^\circ$ Arah %s %s' % (d/1000, b,
                                                   direction, city_name)
    event_info['location_string'] = s



