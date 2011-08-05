import os
import sys

from network.download_shakemap import get_shakemap_data
from modules.event_info import event_info as calculate_event_info
from modules.calculate_location_info import calculate_location_info
from modules.pop_expo import pop_expo as calculate_pop_expo
from modules.city_info import city_info
from modules.cities_on_map import cities_on_map
from modules.region_map import region_map
from modules.city_table import city_table
from modules.mini_indonesia import mini_indonesia
from modules.create_latex_components import generate_event_header
from modules.create_latex_components import generate_exposure_table
from utilities import makedir, make_pdf_filename
from config import shake_url, final_destination

def calculate(shakedata_dir, library_dir, event_name):
    """Calculate exposure information
    """

    event_info, A = calculate_event_info(shakedata_dir, event_name)
    pop_expo, R = calculate_pop_expo(event_info, A, library_dir)
    C = city_info(R, A, library_dir, event_info)
    cities_on_map(C, distance_limit=100)
    vec = (event_info['lat'], event_info['lon'])
    calculate_location_info(event_info, C)
    return event_info, pop_expo, A, R, C


def create_mapcomponents(event_info, event_name, pop_exp, A, R, C):
    """Generate individual pdf components for exposure map
    """

    region_map(event_info, A, R,
               shakedata_dir, event_name, library_dir, basename='exposure_map')
    city_table(C, R, basename='city_legend')
    mini_indonesia(R, library_dir, basename='mini_map')

    # LaTeX contents
    generate_event_header(event_info)
    generate_exposure_table(event_info, pop_expo)


def create_map(event_name):
    """Assemble components into final exposure map
    """

    filename = make_pdf_filename(event_name)
    print 'Compiling map components into %s' % filename

    # Get static files
    os.system('/bin/cp fixtures/* temp')

    # Move generated components into staging area
    os.system('/bin/mv *.pdf temp')
    os.system('/bin/mv *.tex temp')

    # Compile LaTeX document and move it
    os.system('cd temp; pdflatex earthquake_impact_map.tex -s '
              '> ../logs/create_texmap.log')
    os.system('/bin/cp temp/earthquake_impact_map.pdf %s' % filename)

    return filename

def usage(shakedata_dir, shake_url):
    s = ('Usage:\n'
         'python %s [event_name]\n'
         'where event_name is the name of a shake_map tree located '
         'in %s\n'
         'If event_name is omitted latest shakemap from %s will be '
         'used.' % (sys.argv[0], shakedata_dir, shake_url))
    return s

if __name__ == '__main__':

    work_dir = makedir(os.path.join(final_destination, 'dampa'))
    shakedata_dir = os.path.expanduser(os.environ['SHAKEDATA'])
    library_dir = os.path.expanduser(os.environ['IMPACTLIB'])

    makedir('temp')
    makedir('logs')

    # Get shakemap event data
    if len(sys.argv) == 1:
        # Get latest shakemap (in case no event was specified)
        event_name = None
    elif len(sys.argv) == 2:
        # Use event name from command line
        event_name = sys.argv[1]
    else:
        print usage(shakedata_dir, shake_url)
        sys.exit()

    event_name = get_shakemap_data(shake_url, name=event_name,
                                   shakedata_dir=shakedata_dir)

    # Check if this was already made
    filename = make_pdf_filename(event_name)
    if os.path.isfile(os.path.join(work_dir, filename)):
        print ('Impact map %s already exists in %s. No need to compute'
               % (filename, work_dir))
        sys.exit()

    # Calculate
    print 'Calculating population exposure'
    event_info, pop_expo, A, R, C = calculate(shakedata_dir, library_dir,
                                              event_name)

    # Plot Components
    print 'Creating individual map components'
    create_mapcomponents(event_info, event_name, pop_expo, A, R, C)

    # Generate LaTeX document
    filename = create_map(event_name)

    # Copy to web area
    cmd = 'cp -u %s %s' % (filename, work_dir)
    os.system(cmd)

    # Cope to common name for latest (this way the pdf viewer (e.g. evince)
    # will automatically update view). Soft links won't work but a copy is OK.
    latest_name = 'latest_earthquake_impact_map.pdf'
    cmd = 'cd %s; /bin/rm -f %s; cp %s %s' % (work_dir,
                                              latest_name,
                                              filename,
                                              latest_name)

    os.system(cmd)



