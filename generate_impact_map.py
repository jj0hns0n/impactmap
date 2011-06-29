import os
import sys

from network.download_shakemap import get_shakemap_data
from modules.event_info import event_info as calculate_event_info
from modules.pop_expo import pop_expo as calculate_pop_expo
from modules.city_info import city_info
from modules.cities_on_map import cities_on_map
from modules.list_historical_events import list_historical_events
from modules.test_GMT import region_map
from modules.city_table import city_table
from modules.mini_indonesia import mini_indonesia
from modules.exposure import exposure
from modules.create_latex_components import generate_event_header
from utilities import makedir

def calculate(shakedata_dir, library_dir, event_name):
    """Calculate exposure information
    """

    event_info, A = calculate_event_info(shakedata_dir, event_name)
    pop_expo, R = calculate_pop_expo(event_info, A, library_dir)
    C = city_info(R, A, library_dir)
    cities_on_map(C, 100)
    vec = (event_info['lat'], event_info['lon'])
    hist_eve = list_historical_events(vec, library_dir)

    return event_info, pop_expo, A, R, C


def create_mapcomponents(event_info, event_name, pop_exp, A, R, C):
    """Generate individual pdf components for exposure map
    """

    region_map(event_info, A, R,
               shakedata_dir, event_name, library_dir, basename='exposure_map')
    city_table(C, R, basename='city_legend')
    mini_indonesia(R, library_dir, basename='mini_map')
    exposure(pop_expo, library_dir, R, basename='exposure_legend')

    # LaTeX contents
    generate_event_header(event_info)

def create_map():
    """Assemble components into final exposure map
    """

    print 'Compiling map components into earth_quake_impact_map.pdf'

    # Get static files
    os.system('/bin/cp fixtures/* temp')

    # Move generated components into staging area
    os.system('/bin/mv *.pdf temp')
    os.system('/bin/mv *.tex temp')

    # Compile LaTeX document and move it
    #os.system('cd temp; pdflatex earthquake_impact_map.tex -s > ../logs/create_texmap.log')
    os.system('cd temp; pdflatex earthquake_impact_map.tex -s')
    os.system('/bin/cp temp/earthquake_impact_map.pdf .')

def usage(shakedata_dir, shake_url):
    s = ('Usage:\n'
         'python %s [event_name]\n'
         'where event_name is the name of a shake_map tree located '
         'in %s\n'
         'If event_name is omitted latest shakemap from %s will be '
         'used.' % (sys.argv[0], shakedata_dir, shake_url))
    return s

if __name__ == '__main__':

    shakedata_dir = os.environ['SHAKEDATA']
    library_dir = os.environ['IMPACTLIB']
    shake_url = 'ftp://geospasial.bnpb.go.id'

    makedir('temp')
    makedir('logs')

    if len(sys.argv) == 1:
        # Get latest shakemap (in case no event was specified)
        event_name = get_shakemap_data(shake_url)
    elif len(sys.argv) == 2:
        # Use event name from command line
        event_name = sys.argv[1]

        # If it doesn't exist, try to get it from web site
        if not os.path.isdir((os.path.join(shakedata_dir, event_name))):
            event_name = get_shakemap_data(shake_url, event_name)

    else:
        print usage(shakedata_dir, shake_url)
        sys.exit()

    # Calculate
    event_info, pop_expo, A, R, C = calculate(shakedata_dir, library_dir,
                                              event_name)

    # Plot Components
    create_mapcomponents(event_info, event_name, pop_expo, A, R, C)

    # Generate LaTeX document
    create_map()


