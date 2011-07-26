import unittest
import numpy
import sys
import os

from modules.event_info import event_info as calculate_event_info
from modules.pop_expo import pop_expo as calculate_pop_expo

#-------------------------------------------------------------

os.environ['SHAKEDATA'] = 'testdata'

class TestCase(unittest.TestCase):

    def test_examples_run(self):
        """All test examples run to completion
        """

        print
        for event in os.listdir('testdata'):
            if not event.startswith('.'):
                cmd = 'python generate_impact_map.py %s > /dev/null' % event
                print cmd
                err = os.system(cmd)

                msg = 'Event %s failed with error code %i' % (event, err)
                assert err == 0, msg
                assert os.path.isfile('eartquake_impact_map_%s.pdf' % event)


    def test_usgs_cases(self):
        """Calculated values match those from the USGS
        """

        shakedata_dir = os.environ['SHAKEDATA']
        library_dir = os.environ['IMPACTLIB']

        reference_exposure = {'usgs_20110614': {'II+III': 120000,
                                                'IV': 12894000,
                                                'V': 2067000,
                                                'VI': 30000,
                                                'VII': 2000,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0},
                              'usgs_20110716': {'II+III': 532000,
                                                'IV': 0,
                                                'V': 0,
                                                'VI': 0,
                                                'VII': 0,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0}}


        for event_name in os.listdir('testdata'):
            if not event_name.startswith('.') and event_name.startswith('usgs'):

                # Check the MMI values
                event_info, A = calculate_event_info(shakedata_dir, event_name)

                max_mmi = -sys.maxint
                for i in range(A.shape[0]):
                    if A[i,4] > max_mmi:
                        max_mmi = A[i,4]

                # Get reference mmi from data file
                ref_mmi = []
                fid = open(os.path.join(shakedata_dir, event_name, 'output', 'grid.xyz'))
                for line in fid.readlines()[1:]:
                    fields = line.split()
                    ref_mmi.append(float(fields[4]))

                msg = 'Wrong MMI values encountered in event: %s' % event_name
                assert numpy.allclose(ref_mmi, A[:,4]), msg

                # Population data
                pop_expo, R = calculate_pop_expo(event_info, A, library_dir)

                # All the direct comparisons
                for key in ['IV', 'V', 'VI', 'VII', 'VIII', 'IX']:
                    msg = ('Estimated exposure to MMI %s failed for '
                           'event %s: Got %.0f expected %.0f' % (key,
                                                             event_name,
                                                             pop_expo[key],
                                                             reference_exposure[event_name][key]))
                    assert numpy.allclose(pop_expo[key],
                                          reference_exposure[event_name][key],
                                          rtol=1.0e-1, atol=1.0e-1), msg

                # Special case
                s = pop_expo['II'] + pop_expo['III']
                msg = ('Estimated exposure to MMI levels II and III failed for '
                       'event %s: Got %.0f expected %.0f' % (event_name,
                                                         s,
                                                         reference_exposure[event_name]['II+III']))

                assert numpy.allclose(s, reference_exposure[event_name]['II+III'], rtol=1.0e-1, atol=1.0e-1), msg



#-------------------------------------------------------------

if __name__ == "__main__":
    mysuite = unittest.makeSuite(TestCase, 'test_usgs')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(mysuite)



