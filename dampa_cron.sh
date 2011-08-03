#!/usr/bin/bash

# Example of crontab entry
#03 * * * * nielso cd /home/nielso/sandpit/impact_map; sh dampa_cron.sh > dampa_cron.log 2>&1

. ~/shake_env/bin/activate
export SHAKEDATA=~/shakedata
export IMPACTLIB=~/impactlib
python generate_impact_map.py
python get_shakemap_data.py
