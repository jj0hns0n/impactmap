import numpy

try:
    from scipy.interpolate import griddata
except:
    from matplotlib.mlab import griddata
    griddata_version = 'pylab'
else:
    griddata_version = 'scipy'


def make_grid(points, values, grid, method=None):
    """Abstraction of two different versions of griddata

    points: Nx2 array of points where data is known
    values: corresponding values
    grid: Tuple of X, Y - Regular grid (e.g. obtained from meshgrid)
    """


    if griddata_version == 'scipy':
        if method is None:
            m = 'cubic'
        else:
            m = method

        return griddata(points, values, grid, method=m)
    elif griddata_version == 'pylab':
        if method is None:
            m = 'nn'
        else:
            m = method

        x = points[:,0]
        y = points[:,0]
        z = values
        X, Y = grid
        return griddata(x, y, z, X, Y, interp=m)
