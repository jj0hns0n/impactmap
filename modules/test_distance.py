"""Small test of the points2distance code
"""

import unittest
import numpy
from points2distance import points2distance

#-------------------------------------------------------------

class TestCase(unittest.TestCase):

    def testEarthquake2Muncar(self):
        # Data from http://www.movable-type.co.uk/scripts/latlong.html
        D = 151.300   # True Distance [m]

        EQ_lat = -9.65
        EQ_lon = 113.72

        Muncar_lat = -8.43
        Muncar_lon = 114.33

        # Calculate distance using the points2distance code
        #start = ((Muncar_lat,0,0),(Muncar_lon,0,0))
        #end = ((EQ_lat,0,0),(EQ_lon,0,0))

        start = ((Muncar_lon,0,0),(Muncar_lat,0,0))
        end = ((EQ_lon,0,0),(EQ_lat,0,0))
        d = points2distance(start,end)

        msg = 'Dist to Muncar failed, was %f expected %f' % (d, D)
        assert numpy.allclose(d, D), msg



#-------------------------------------------------------------
if __name__ == "__main__":
    mysuite = unittest.makeSuite(TestCase,'test')
    runner = unittest.TextTestRunner()
    runner.run(mysuite)

