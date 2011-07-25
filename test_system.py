import unittest
import numpy
import os

#-------------------------------------------------------------

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




#-------------------------------------------------------------

if __name__ == "__main__":
    mysuite = unittest.makeSuite(TestCase, 'test')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(mysuite)



