import numpy

try:
    from scipy.interpolate import griddata
except:
    from matplotlib.mlab import griddata
    griddata_version = 'pylab'
else:
    griddata_version = 'scipy'


def make_grid(x, y, z, X, Y, method=None):
    """Abstraction of two different versions of griddata

    x, y, z: Irregular points
    X, Y: Regular grid (e.g. obtained from meshgrid)
    """

    if griddata_version == 'scipy':
        if method is None:
            m = 'cubic'
        else:
            m = method
        return griddata([x, y], z, [X, Y], method=m)
    elif griddata_version == 'pylab':
        if method is None:
            m = 'nn'
        else:
            m = method
        return griddata(x, y, z, X, Y, interp=m)
