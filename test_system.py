import unittest
import numpy
import sys
import os

from modules.event_info import event_info as calculate_event_info
from modules.pop_expo import pop_expo as calculate_pop_expo
from modules.city_info import city_info
from modules.cities_on_map import cities_on_map


os.environ['SHAKEDATA'] = 'testdata'
shakedata_dir = os.environ['SHAKEDATA']
library_dir = os.environ['IMPACTLIB']


class TestCase(unittest.TestCase):


    def test_city_placement_on_map(self):
        """Cities are placed correctly on map
        """

        event_name = 'BNPB-SCENARIO'

        expected_result = {10: ['Loa',
                                'Samarinda',
                                'Balikpapan',
                                'Bontang',
                                'Palu',
                                'Majene',
                                'Rantepao',
                                'Poso',
                                'Baolan',
                                'Polewali',
                                'Pare',
                                'Kota',
                                'Palopo'],
                           100: ['Loa',
                                 'Palu',
                                 'Majene',
                                 'Rantepao',
                                 'Poso',
                                 'Baolan',
                                 'Kota'],
                           200: ['Loa',
                                 'Palu',
                                 'Majene',
                                 'Kota'],
                           500: ['Loa']}

        # Run test for a range of distance limits
        for d in [10]: #, 100, 200, 500]:

            # Clean up first. FIXME (Ole): Move this to function
            cmd = '/bin/rm -rf city.txt'
            os.system(cmd)

            # Check that reference data exists
            msg = 'There is no reference data for distance_limit %i' % d
            assert d in expected_result, msg

            # Run
            event_info, A = calculate_event_info(shakedata_dir, event_name)
            pop_expo, R = calculate_pop_expo(event_info, A, library_dir)
            C = city_info(R, A, library_dir, event_info)
            cities_on_map(C, distance_limit=d)

            # Verify result against reference data
            fid = open('city.txt')
            for i, line in enumerate(fid.readlines()):
                print line.strip()
                fields = line.strip().split()
                city = fields[-1]

                try:
                    ref_city = expected_result[d][i]
                except IndexError, e:
                    msg = ('%s: Insufficient reference data for '
                           'distance_limit %i and city %s. '
                           'Invalid index was %i'
                           % (e, d, city, i))
                    raise Exception(msg)

                # Check that city names match
                msg = ('Cities do not match: Got %s but expected %s'
                       % (city, ref_city))
                assert city == ref_city, msg


        # Clean up
        cmd = '/bin/rm -rf city.txt'
        os.system(cmd)


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
                              'usgs_20100509': {'II+III': 1034000, # Checked
                                                'IV': 8907000,
                                                'V': 1906000,
                                                'VI': 279000,
                                                'VII': 397000,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0},
                              'usgs_20090930': {'II+III': 269000, # Checked
                                                'IV': 2299000,
                                                'V': 6350000,
                                                'VI': 1715000,
                                                'VII': 3318000,
                                                'VIII': 1010000,
                                                'IX': 0,
                                                'X': 0},
                              'usgs_20090902': {'II+III': 8204000, # Checked
                                                'IV': 45112000,
                                                'V': 25796000,
                                                'VI': 3247000,
                                                'VII': 719000,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0},
                              'usgs_20110403': {'II+III': 44746000, # Checked
                                                'IV': 22000,
                                                'V': 0,
                                                'VI': 0,
                                                'VII': 0,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0},
                              'usgs_20110424': {'II+III': 10000, # Checked
                                                'IV': 3659000,
                                                'V': 1220000,
                                                'VI': 254000,
                                                'VII': 115000,
                                                'VIII': 16000,
                                                'IX': 0,
                                                'X': 0},
                              'usgs_20081116': {'II+III': 1112000, # Checked
                                                'IV': 2505000,
                                                'V': 895000,
                                                'VI': 653000,
                                                'VII': 184000,
                                                'VIII': 68,
                                                'IX': 0,
                                                'X': 0},
                             'usgs_20110626': {'II+III': 919000,  # Checked
                                                'IV': 347000,
                                                'V': 83000,
                                                'VI': 15000,
                                                'VII': 21,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0},
                             'usgs_20101026': {'II+III': 3554000, # Checked
                                                'IV': 186000,
                                                'V': 24000,
                                                'VI': 8000,
                                                'VII': 0,
                                                'VIII': 0,
                                                'IX': 0,
                                                'X': 0},
                            'usgs_20101116': {'II+III': 0, # Checked
                                              'IV': 551000,
                                              'V': 49000,
                                              'VI': 11000,
                                              'VII': 8000,
                                              'VIII': 1000,
                                              'IX': 0,
                                              'X': 0},
                           'usgs_20110215': {'II+III': 93000, # Checked
                                             'IV': 11518000,
                                             'V': 258000,
                                             'VI': 32000,
                                             'VII': 279000,
                                             'VIII': 2000,
                                             'IX': 0,
                                             'X': 0},
                           'usgs_20110526': {'II+III': 2000, # Checked
                                             'IV': 1654000,
                                             'V': 515000,
                                             'VI': 85,
                                             'VII': 1000,
                                             'VIII': 0,
                                             'IX': 0,
                                             'X': 0}}
        skip = []
        mismatched = 0
        within_10pct = 0
        between_10_and_20pct = 0
        maxerr = 0
        minerr = 0
        errcount = 0
        errsum = 0
        print

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

                    denom = max(pop_expo[key], reference_exposure[event_name][key])
                    if denom > 0:
                        err = abs(pop_expo[key] - reference_exposure[event_name][key])/denom
                    else:
                        err = abs(pop_expo[key] - reference_exposure[event_name][key])

                    if err > maxerr:
                        maxerr = err

                    if err < minerr:
                        minerr = err

                    errsum += err
                    errcount += 1


                    if numpy.allclose(pop_expo[key],
                                      reference_exposure[event_name][key],
                                      rtol=1e-1, atol=1000) or abs(pop_expo[key] - reference_exposure[event_name][key]) < 5000:
                        within_10pct += 1
                        #print 'Match', event_name, key, pop_expo[key], reference_exposure[event_name][key]
                    elif numpy.allclose(pop_expo[key],
                                      reference_exposure[event_name][key],
                                      rtol=2.0e-1, atol=1000):
                        between_10_and_20pct += 1
                    else:
                        mismatched += 1
                        print 'Mismatch', event_name, key, pop_expo[key], reference_exposure[event_name][key], err

                    #assert numpy.allclose(pop_expo[key],
                    #                      reference_exposure[event_name][key],
                    #                      rtol=1.0e-1, atol=1.0e-1), msg

                # Special case - FIXME (Ole): Why are these generally so bad?
                s = pop_expo['II'] + pop_expo['III']
                #print 'sum', pop_expo['II'], pop_expo['III']
                #msg = ('Estimated exposure to MMI levels II and III failed for '
                #      'event %s: Got %.0f expected %.0f' % (event_name,
                #                                            s,
                #                                            reference_exposure[event_name]['II+III']))

                # key = 'II+III'
                # denom = max(s, reference_exposure[event_name][key])
                # if denom > 0:
                #     err = abs(s - reference_exposure[event_name][key])/denom
                # else:
                #     err = abs(s - reference_exposure[event_name][key])

                # if err > maxerr:
                #     maxerr = err

                # if err < minerr:
                #     minerr = err

                # errsum += err
                # errcount += 1


                # if numpy.allclose(s,
                #                   reference_exposure[event_name][key],
                #                   rtol=1e-1, atol=1000) or abs(s - reference_exposure[event_name][key]) < 5000:
                #     within_10pct += 1
                # elif numpy.allclose(s,
                #                     reference_exposure[event_name][key],
                #                     rtol=2.0e-1, atol=1000):
                #     between_10_and_20pct += 1
                # else:
                #     mismatched += 1
                #     print 'Mismatch', event_name, key, s, reference_exposure[event_name][key], err

        #print
        mismatch_ratio = float(mismatched)/(within_10pct+between_10_and_20pct+mismatched)
        print 'Number of matches within 10%', within_10pct
        print 'Number of matches between 10% and 20%:', between_10_and_20pct
        print 'Number of mismatches', mismatched
        print 'Ratio of mismatched:', mismatch_ratio

        print 'Max error:', maxerr
        print 'Min error:', minerr
        print 'Avg error:', errsum/errcount

        assert within_10pct > 70

        msg = 'Ratio of comparisons with error worse than 20% exceeded target 0.03'
        assert mismatch_ratio < 0.03, msg


#-------------------------------------------------------------

if __name__ == "__main__":
    mysuite = unittest.makeSuite(TestCase, 'test')
    mysuite = unittest.makeSuite(TestCase, 'test_city')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(mysuite)



