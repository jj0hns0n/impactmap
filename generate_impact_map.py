import os
from modules.event_info import event_info
from modules.pop_expo import pop_expo
from modules.city_info import city_info
from modules.cities_on_map import cities_on_map
from modules.list_historical_events import list_historical_events
from modules.test_GMT import region_map
from modules.city_table import city_table
from modules.mini_indonesia import mini_indonesia
from modules.exposure import exposure
from utilities import makedir

shakedata_dir = os.environ['SHAKEDATA']
library_dir = os.environ['IMPACTLIB']

# Calculate
event_info,A = event_info(shakedata_dir)
pop_expo,R = pop_expo(event_info,A,library_dir)
C = city_info(R,A,library_dir)
cities_on_map(C,100)
vec = (event_info['lat'],event_info['lon'])
hist_eve = list_historical_events(vec,library_dir)

# Plot Components
region_map(event_info, A, R,
           shakedata_dir, library_dir, basename='exposure_map')
city_table(C, R, basename='city_legend')
mini_indonesia(R, library_dir, basename='mini_map')
exposure(pop_expo, library_dir, R, basename='exposure_legend')

# Generate LaTeX document
makedir('temp')
os.system('/bin/cp fixtures/* temp')
os.system('/bin/mv *.pdf temp')
os.system('cd temp; pdflatex earthquake_impact_map.tex')
os.system('/bin/cp temp/earthquake_impact_map.pdf .')
