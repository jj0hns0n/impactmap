import numpy
import points2distance
import os


def cities_on_map(A, distance_limit=100):
    """Put selected cities on map.

    Ensure that cities shown are at least dis_lim km apart.

    Input
        A: Selected cities sorted by intensity and population.
        distance_limit: Minimum distance [km] between cities shown on map (default is 100 km)

    Output
        Generates text file for use by GMT to plot cities on map
    """

    # Always take the first city (which is the one with the highest intensity)
    index = [0]

    # Indices of all remaining cities
    T = range(1, len(A))

    # Loop through remaining cities and determine which to plot
    T2 = []
    b = 0
    while True:

        # Find cities more than distance_limit km away from city b (anchor city)
        for i in range(len(T)):
            start = ((A['lon'][b],0,0),(A['lat'][b],0,0))      # Anchor city
            end = ((A['lon'][T[i]],0,0),(A['lat'][T[i]],0,0))  # Other city
            r = points2distance.points2distance(start,end)
            if r >= distance_limit:
                # Select city i because it is sufficiently far away from anchor city
                T2 += [(T[i])]

        # Determine whether to use more cities or not
        if len(T2) > 1:
            # If more than one candidate exist pick the first of the selected cities as new anchor city
            b = T2[0]
            index += [(b)]

            # Replace T with what now remains and reset T2
            T = T2[1:]
            T2 = []
        elif len(T2) == 1:
            # If only one city exists add it and exit loop
            index += [(T2[0])]
            break
        else:
            # If no cities were found exit loop
            break

    # Record selected cities in GMT file
    for i in index:
        cmd = 'cat << END >> city.txt'+'\n'+''+str(A['lon'][i])+' '+str(A['lat'][i])+' 15 0 0 BR '+A['name'][i]+'\n'+'END'
        os.system(cmd)








