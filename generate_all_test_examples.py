"""Generate pdf for all examples in testdata
"""

import os

os.environ['SHAKEDATA'] = 'testdata'
for event in os.listdir('testdata'):
    if not event.startswith('.'):
        cmd = 'python generate_impact_map.py %s > /dev/null' % event
        err = os.system(cmd)

        msg = 'Event %s failed with error code %i' % (event, err)
        assert err == 0, msg
        assert os.path.isfile('eartquake_impact_map_%s.pdf' % event)

        cmd = 'cp eartquake_impact_map_%s.pdf testdata' % event
        os.system(cmd)
