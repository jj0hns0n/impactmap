"""Download and process shakemap data
"""

import sys
import os

from network.download_shakemap import get_shakemap_data

if __name__ == '__main__':

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
    cmd = ('cp %s/%s/output/mi.grd %s'
           % (shakedata_dir, event_name, grd_filename))
    print cmd
    os.system(cmd)

    # Convert grd file to asc and tif
    cmd = 'python convert_gmt_grid.py %s' % grd_filename
    os.system(cmd)

    # Contour tif file
    cmd = '/bin/rm -rf %s' % shp_filename
    os.system(cmd)

    cmd = 'gdal_contour -i %f %s %s' % (1, tif_filename, shp_filename)
    print cmd
    os.system(cmd)

    print
    print 'Finished receiving shakemap data'
    print 'Shakemap surface available in: %s and %s' % (asc_filename,
                                                        tif_filename)
    print 'Shakemap contour available in: %s' % shp_filename

    # View in QGIS
    #basemap = '%s/maps/Basemap_300dpi.tif' % library_dir
    #cmd = 'qgis %s %s %s &' % (basemap, tif_filename, shp_filename)
    #os.system(cmd)
