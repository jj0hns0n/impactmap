"""point.py - Represents a generic point on a sphere as a Python object.

   See documentation of class Point for details.
   Ole Nielsen, ANU 2002
"""


from math import cos, sin, pi

def acos(c):
  """acos -  Safe inverse cosine

     Input argument c is shrunk to admissible interval
     to avoid case where a small rounding error causes
     a math domain error.
  """
  from math import acos

  if c > 1: c=1
  if c < -1: c=-1

  return acos(c)


class Point:
    """Definition of a generic point on the sphere.

    Defines a point in terms of latitude and longitude
    and computes distances to other points on the sphere.

    Initialise as
      Point(lat, lon), where lat and lon are in decimal degrees (dd.dddd)

    Public Methods:
        distance_to(P)
        bearing_to(P)
        dist(P)

    Author: Ole Nielsen, ANU 2002
    """

    # class constants
    R = 6372000  # Approximate radius of Earth (m)
    degrees2radians = pi/180.0


    def __init__(self, latitude=None, longitude=None):

        if latitude is None:
            msg = 'Argument latitude must be specified to Point constructor'
            raise Exception(msg)

        if longitude is None:
            msg = 'Argument longitude must be specified to Point constructor'
            raise Exception(msg)

        msg = 'Specified latitude %f was out of bounds' % latitude
        assert(latitude >= -90 and latitude <= 90.0), msg

        msg = 'Specified longitude %f was out of bounds' % longitude
        assert(longitude >= -180 and longitude <= 180.0), msg

        self.latitude = float(latitude)
        self.longitude = float(longitude)

        lat = latitude * self.degrees2radians    # Converted to radians
        lon = longitude * self.degrees2radians   # Converted to radians
        self.coslat = cos(lat)
        self.coslon = cos(lon)
        self.sinlat = sin(lat)
        self.sinlon = sin(lon)


    #---------------
    # Public methods
    #---------------

    def bearing_to(self, P):
        """Bearing (in degrees) to point P"""
        AZ = self.AZ(P)
        return int(round(AZ/self.degrees2radians))

    def distance_to(self, P):
        """Distance to point P"""
        GCA = self.GCA(P)
        return self.R*GCA

    def approximate_distance_to(self, P):
        """Very cheap and rough approximation to distance"""

        return max(abs(self.latitude-P.latitude),
                   abs(self.longitude-P.longitude))


    #-----------------
    # Internal methods
    #-----------------

    def __repr__(self):
        """Readable representation of point
        """
        d = 2
        lat = round(self.latitude,d)
        lon = round(self.longitude,d)
        return ' (' + str(lat)+ ', '+ str(lon)+')'

    def GCA(self, P):
        """Compute the Creat Circle Angle (GCA) between current point and P
        """

        alpha = P.coslon*self.coslon + P.sinlon*self.sinlon
        # The original formula is alpha = cos(self.lon - P.lon)
        # but rewriting lets us make us of precomputed trigonometric values.

        x = alpha*self.coslat*P.coslat + self.sinlat*P.sinlat
        return acos(x)


    def AZ(self, P):
        """Compute Azimuth bearing (AZ) from current point to P
        """

        # Compute cosine(AZ), where AZ is the azimuth angle
        GCA = self.GCA(P)
        c = P.sinlat - self.sinlat*cos(GCA)
        c = c/self.coslat/sin(GCA)

        AZ = acos(c)

        # Reverse direction if bearing is westward,
        # i.e. sin(self.lon - P.lon) > 0
        # Without this correction the bearing due west, say, will be 90 degrees
        # because the formulas work in the positive direction which is east.
        #
        # Precomputed trigonometric values are used to rewrite the formula:

        if self.sinlon*P.coslon - self.coslon*P.sinlon > 0: AZ = 2*pi - AZ

        return AZ


#---------------------------------------------
# NOTE (Ole): Not in use, but could be needed one day
def safe_acos(x):
    """Safely compute acos

       Protect against cases where input argument x is outside the allowed
       interval [-1.0, 1.0] by no more than machine precision

       Ole Nielsen 2006
    """

    error_msg = ('Input to acos is outside allowed domain [-1.0, 1.0].'
                 'I got %.12f' % x)
    warning_msg = 'Changing argument to acos from %.18f to %.1f' % (x, sign(x))

    eps = get_machine_precision() # Machine precision

    if x < -1.0:
        if x < -1.0 - eps:
            raise ValueError, errmsg
        else:
            warn(warning_msg)
            x = -1.0

    if x > 1.0:
        if x > 1.0 + eps:
            raise ValueError, errmsg
        else:
            print 'NOTE: changing argument to acos from %.18f to 1.0' % x
            x = 1.0

    return acos(x)


def get_machine_precision():
    """Calculate the machine precision for Floats

       Depends on static variable machine_precision in this module
       as this would otherwise require too much computation.
    """

    global machine_precision

    if machine_precision is None:
        epsilon = 1.
        while epsilon/2 + 1. > 1.:
            epsilon /= 2

        machine_precision = epsilon

    return machine_precision
