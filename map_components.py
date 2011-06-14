"""Generate the various map components for EQI
"""

# NOTE - this early version assumes that the files
# - Indonesia.topobath.1m.grd
# - topo_grad.grd
# are located in the current working directory.


import os
from fixtures import PLTEMPLATE

class GMT:
    """Class for representing attributes and methods common to GMT plots
    """

    def __init__(self,
                 font='1', font_heading='1',
                 fontsize='9', fontsize_heading='16',
                 shore_colour='10/40/100', water_colour = '120/160/220'):

        self.font = font
        self.fontsize = fontsize
        self.font_heading = font_heading
        self.fontsize_heading = fontsize_heading
        self.shore_colour = shore_colour
        self.water_colour = water_colour

        # Set global GMT variables
        os.system('gmtset ANNOT_FONT_SIZE_PRIMARY 9p ANNOT_FONT_PRIMARY 1')
        os.system('gmtset ANNOT_OFFSET_PRIMARY = 0.15c PLOT_DEGREE_FORMAT ddd:mm:ss')
        os.system('gmtset BASEMAP_TYPE = plain')

        # FIXME: Need to sort out GMT command for setting global projection
        # and bounding box globally

    def population_legend(self):
        """Generate legend for population density
        """

        # Generate raw postscript for legend
        legend_filename = 'pop-legend.txt'

        fid = open(legend_filename, 'w')
        fid.write(PLTEMPLATE % ((self.font, self.fontsize)*4))
        fid.close()

        # Plot legend
        filename = 'population_legend.eps'

        # Some options hardwired for the purpose of this example
        #options = '-Dx0.2i/0.9i/1.5i/0.9i/TL -J -R -P'
        R = '94.9765016667/101.066/0.053/6.06944566667'
        J = 'Q4.75i'
        options = '-Dx0.2i/0.9i/1.5i/0.9i/TL -J%s -R%s -P' % (J, R)
        cmd = 'pslegend %s %s' % (options, legend_filename)
        os.system('%s > %s' % (cmd, filename))

        # Return generated filename
        return filename

    def minimap(self, inset):
        """Generate minimap with inset
        """

        # Create palette
        palette_filename = 'palette.cpt'
        cmd = 'makecpt -Crelief -T-9200/9200/100 -Z'
        os.system('%s > %s' % (cmd, palette_filename))

        # Write footprint (maybe move to constructor later)
        inset_filename = 'event_footprint.txt'
        fid = open(inset_filename, 'w')
        for i in range(len(inset)):
            fid.write('%.5f, %.5f\n' % (inset[i][0], inset[i][1]))
        fid.close()

        # Create map of Indonesia
        minimap_filename = 'minimap.eps'
        options = '-B10d -R94/141.5/-11.5/6 -JM2.5i -K -P'
        cmd = 'grdimage %s -I %s %s -C%s' % ('Indonesia.topobath.1m.grd',
                                             'topo_grad.grd',
                                             options,
                                             palette_filename)
        os.system('%s > %s' % (cmd, minimap_filename))

        options = '-O -P -JM2.5i -W1.5p,red -R94/143/-12/7'
        cmd = 'psxy %s %s' % (options, inset_filename)
        os.system('%s >> %s' % (cmd, minimap_filename))

        # Return generated filename
        return minimap_filename


if __name__ == '__main__':
    g = GMT()
    g.population_legend()
    g.minimap([[94.9765, 6.069446],
               [101.066, 6.069446],
               [101.066, 0.053],
               [94.9765, 0.053],
               [094.9766, 6.06945]])
