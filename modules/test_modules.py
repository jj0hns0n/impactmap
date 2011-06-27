import os
from event_info import event_info
from pop_expo import pop_expo
from city_info import city_info
from cities_on_map import cities_on_map
from list_historical_events import list_historical_events
from test_GMT import region_map
from city_table import city_table
from mini_indonesia import mini_indonesia
from exposure import exposure

shakedata_dir = os.environ['SHAKEDATA']
library_dir = os.environ['IMPACTLIB']

event_info,A = event_info(shakedata_dir)
pop_expo,R = pop_expo(event_info,A,library_dir)
C = city_info(R,A,library_dir)
cities_on_map(C,100)
vec = (event_info['lat'],event_info['lon'])
hist_eve = list_historical_events(vec,library_dir)


# Plot Components
region_map(event_info,A,R,shakedata_dir,library_dir)
city_table(C,R)
mini_indonesia(R,library_dir)
exposure(pop_expo,library_dir,R)
