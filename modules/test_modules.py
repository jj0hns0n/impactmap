import os
from event_info import event_info
from pop_expo import pop_expo
from city_info import city_info
from cities_on_map import cities_on_map
from list_historical_events import list_historical_events

shakedata_dir = os.environ['SHAKEDATA']
library_dir = os.environ['IMPACTLIB']

event_info,A = event_info(shakedata_dir)
pop_expo,R = pop_expo(event_info,A,library_dir)
C = city_info(R,A,library_dir)
cities_on_map(C,100)
vec = (event_info['lat'],event_info['lon'])
hist_eve = list_historical_events(vec,library_dir)

#print hist_eve
#print C['intensity']

