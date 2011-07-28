"""Download and process shakemap data
"""

import sys
import os
from network.download_shakemap import get_shakemap_data
from utilities import makedir

if __name__ == '__main__':

    work_dir = makedir('shakemap_data')

    shakedata_dir = os.environ['SHAKEDATA']
    library_dir = os.environ['IMPACTLIB']
    shake_url = 'ftp://geospasial.bnpb.go.id'

    # Get shakemap event data
    if len(sys.argv) == 1:
        # Get latest shakemap (in case no event was specified)
        event_name = None
    elif len(sys.argv) == 2:
        # Use event name from command line
        event_name = sys.argv[1]
    else:
        print usage(shakedata_dir, shake_url)
        sys.exit()

    event_name = get_shakemap_data(shake_url, event_name)

    # Extract original shakemap information as GIS
    grd_filename = event_name + '.grd'
    asc_filename = event_name + '.asc'
    tif_filename = event_name + '.tif'
    shp_filename = event_name + '.shp'
    cmd = ('cp %s/%s/output/mi.grd %s/%s'
           % (shakedata_dir, event_name, work_dir, grd_filename))
    print cmd
    os.system(cmd)

    # Convert grd file to asc and tif
    cmd = 'python convert_gmt_grid.py %s/%s' % (work_dir, grd_filename)
    os.system(cmd)

    # Contour tif file
    cmd = '/bin/rm -rf %s/%s' % (work_dir, shp_filename)
    os.system(cmd)

    cmd = 'cd %s; gdal_contour -i %f %s %s' % (work_dir, 1,
                                               tif_filename, shp_filename)
    print cmd
    os.system(cmd)

    print
    print 'Finished receiving shakemap data'
    print ('Shakemap surface available in: %s/%s '
           'and %s/%s' % (work_dir, asc_filename, work_dir, tif_filename))
    print 'Shakemap contour available in: %s/%s' % (work_dir, shp_filename)

    # View in QGIS
    #basemap = '%s/maps/Basemap_300dpi.tif' % library_dir
    #cmd = 'cd %s; qgis %s %s %s &' % (work_dir, basemap,
    #                                  tif_filename, shp_filename)
    #os.system(cmd)
