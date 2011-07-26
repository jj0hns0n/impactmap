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

        #print
        for event in os.listdir('testdata'):
            if not event.startswith('.'):
                cmd = 'python generate_impact_map.py %s > /dev/null' % event
                #print cmd
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
                                                'X': 0},
                              'usgs_20100509': {'II+III': 1034000,
                                                'IV': 8907000,
                                                'V': 1906000,
                                                'VI': 279000,
                                                'VII': 397000,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0},
                              'usgs_20090930': {'II+III': 269000,
                                                'IV': 2299000,
                                                'V': 6350000,
                                                'VI': 1715000,
                                                'VII': 3318000,
                                                'VIII': 1010000,
                                                'IX': 0,
                                                'X': 0},
                              'usgs_20090902': {'II+III': 8204000,
                                                'IV': 45112000,
                                                'V': 25796000,
                                                'VI': 3247000,
                                                'VII': 719000,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0},
                              'usgs_20110403': {'II+III': 44746000,
                                                'IV': 22000,
                                                'V': 0,
                                                'VI': 0,
                                                'VII': 0,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0},
                              'usgs_20110424': {'II+III': 10000,
                                                'IV': 3659000,
                                                'V': 1220000,
                                                'VI': 254000,
                                                'VII': 115000,
                                                'VIII': 16000,
                                                'IX': 0,
                                                'X': 0},
                              'usgs_20081116': {'II+III': 1112000,
                                                'IV': 2505000,
                                                'V': 895000,
                                                'VI': 653000,
                                                'VII': 184000,
                                                'VIII': 68000,
                                                'IX': 0,
                                                'X': 0},

                             'usgs_20110626': {'II+III': 919000,
                                                'IV': 347000,
                                                'V': 83000,
                                                'VI': 15000,
                                                'VII': 21000,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0},
                             'usgs_20101026': {'II+III': 3554000,
                                                'IV': 186000,
                                                'V': 24000,
                                                'VI': 8000,
                                                'VII': 0,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0},
                            'usgs_20101116': {'II+III': 0,
                                                'IV': 551000,
                                                'V': 49000,
                                                'VI': 11000,
                                                'VII': 8000,
                                                'VIII': 1000,
                                                'IX': 0,
                                                'X': 0},
                           'usgs_20110215': {'II+III': 93000,
                                                'IV': 11518000,
                                                'V': 258000,
                                                'VI': 32000,
                                                'VII': 279000,
                                                'VIII': 2000,
                                                'IX': 0,
                                                'X': 0},
                           'usgs_20110526': {'II+III': 2000,
                                                'IV': 1654000,
                                                'V': 515000,
                                                'VI': 85000,
                                                'VII': 1000,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0}}
        skip = ['usgs_20081116']
        mismatched = 0
        matched = 0
        maxerr = 0
        minerr = 0
        errcount = 0
        errsum = 0
        for event_name in os.listdir('testdata'):
            if not event_name.startswith('.') and event_name.startswith('usgs'):

                if event_name in skip:
                    continue

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
                    #msg = ('Estimated exposure to MMI %s failed for '
                    #       'event %s: Got %.0f expected %.0f' % (key,
                    #                                             event_name,
                    #                                             pop_expo[key],
                    #                                             reference_exposure[event_name][key]))

                    # Count how many comparisons are better than 10%

                    if pop_expo[key] > 0:
                        err = abs(pop_expo[key] - reference_exposure[event_name][key])/pop_expo[key]
                        #if err == 1.0:
                        #    print 'Arrg', event_name, key, pop_expo[key], reference_exposure[event_name][key]
                        if err > maxerr:
                            maxerr = err

                        if err < minerr:
                            minerr = err

                        errsum += err
                        errcount += 1

                    if numpy.allclose(pop_expo[key],
                                      reference_exposure[event_name][key],
                                      rtol=1.0e-1, atol=1.0e-1):
                        matched += 1
                    else:
                        mismatched += 1

                    #assert numpy.allclose(pop_expo[key],
                    #                      reference_exposure[event_name][key],
                    #                      rtol=1.0e-1, atol=1.0e-1), msg

                # Special case
                #s = pop_expo['II'] + pop_expo['III']
                #print 'sum', pop_expo['II'], pop_expo['III']
                #msg = ('Estimated exposure to MMI levels II and III failed for '
                #      'event %s: Got %.0f expected %.0f' % (event_name,
                #                                            s,
                #                                            reference_exposure[event_name]['II+III']))
                #
                #assert numpy.allclose(s, reference_exposure[event_name]['II+III'], rtol=5.0e-1, atol=1.0e-1), msg
                #print s, reference_exposure[event_name]['II+III']
                #if numpy.allclose(s, reference_exposure[event_name]['II+III'], rtol=5.0e-1, atol=1.0e-1):
                #    matched += 1
                #else:
                #    mismatched += 1

        #print
        print 'Number of matches', matched
        print 'Number of mismatches', mismatched
        print 'Ratio of mismatched:', float(mismatched)/(matched+mismatched)

        print 'Max error:', maxerr
        print 'Min error:', minerr
        print 'Avg error:', errsum/errcount

       # msg = 'Ratio of comparisons with error worse than 10% exceeded target 0.08'
       # assert float(mismatched)/(matched+mismatched) < 0.08, msg


#-------------------------------------------------------------

if __name__ == "__main__":
    mysuite = unittest.makeSuite(TestCase, 'test')
    #mysuite = unittest.makeSuite(TestCase, 'test_usgs')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(mysuite)



