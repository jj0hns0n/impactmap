import os

from network.download_shakemap import get_latest_shakemap
from network.download_shakemap import unpack
from modules.event_info import event_info as calculate_event_info
from modules.pop_expo import pop_expo as calculate_pop_expo
from modules.city_info import city_info
from modules.cities_on_map import cities_on_map
from modules.list_historical_events import list_historical_events
from modules.test_GMT import region_map
from modules.city_table import city_table
from modules.mini_indonesia import mini_indonesia
from modules.exposure import exposure
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


def create_mapcomponents(event_info, pop_exp, A, R, C):
    """Generate individual pdf components for exposure map
    """

    region_map(event_info, A, R,
               shakedata_dir, library_dir, basename='exposure_map')
    city_table(C, R, basename='city_legend')
    mini_indonesia(R, library_dir, basename='mini_map')
    exposure(pop_expo, library_dir, R, basename='exposure_legend')


def create_map():
    """Assemble components into final exposure map
    """

    makedir('temp')
    os.system('/bin/cp fixtures/* temp')
    os.system('/bin/mv *.pdf temp')
    os.system('cd temp; pdflatex earthquake_impact_map.tex')
    os.system('/bin/cp temp/earthquake_impact_map.pdf .')


if __name__ == '__main__':

    shakedata_dir = os.environ['SHAKEDATA']
    library_dir = os.environ['IMPACTLIB']
    shake_url = 'ftp://geospasial.bnpb.go.id'

    # FIXME: Allow cmdline naming
    # event_name = sys.argv[1]

    # Get latest shakemap (in case no event was specified)
    filename = get_latest_shakemap(shake_url)
    event_name = unpack(filename)

    # Calculate
    event_info, pop_expo, A, R, C = calculate(shakedata_dir, library_dir,
                                              event_name)

    # Plot Components
    create_mapcomponents(event_info, pop_expo, A, R, C)

    # Generate LaTeX document
    create_map()


