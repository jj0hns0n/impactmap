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
    s = 'Berjarak %i km dari %s, arah %i$^\circ$' % (d/1000, city_name, b)
    event_info['location_string'] = s



