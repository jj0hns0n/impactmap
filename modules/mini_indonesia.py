import os
import numpy as np

def mini_indonesia(R, path, basename='comp3'):
    """Generate small map inset showing location of exposure map

    Input
        R:
        path:
        basename: Optional basename for generated pdf file
    """


    relief = path+'/palettes/releif.cpt'
    topo_bath = path+'/topography/Indonesia.topobath.1m.grd'
    topo = path+'/topography/topo_grad.grd'
    footprint = str(R[0]) + '\t' + str(R[3]) + '\n'
    footprint = footprint + str(R[1]) + '\t' + str(R[3]) + '\n'
    footprint = footprint + str(R[1]) + '\t' + str(R[2]) + '\n'
    footprint = footprint + str(R[0]) + '\t' + str(R[2]) + '\n'
    footprint = footprint + str(R[0]) + '\t' + str(R[3])
    r = open('region.txt','w')
    r.write(footprint)
    r.close()
    os.system('psbasemap -R94/143/-12/7 -JM2.5i -K -P -X1 -Y1 -Gwhite > %s.eps' % basename)
    os.system('grdimage '+ topo_bath +' -I' + topo + ' -B10d -R94/141.5/-11.5/6 -K -O -JM2.5i -C'+relief+' >> %s.eps' % basename)
    os.system('psxy region.txt -O -K -P -JM2.5i -W1.5p,red -R94/143/-12/7 >> %s.eps' % basename)

    os.system('ps2pdf14 -dPDFSETTINGS=/prepress -dEPSCrop %s.eps' % basename)
    os.system('pdfcrop %s.pdf %s.pdf' % (basename, basename))
    os.system('rm %s.eps' % basename)
    os.system('rm region.txt')
