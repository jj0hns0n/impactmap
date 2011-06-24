import os
import numpy as np
def mini_indonesia(R,path):
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
    os.system('psbasemap -R94/143/-12/7 -JM2.5i -K -P -X1 -Y1 -Gwhite > comp3.eps')
    os.system('grdimage '+ topo_bath +' -I' + topo + ' -B10d -R94/141.5/-11.5/6 -K -O -JM2.5i -C'+relief+' >>comp3.eps')
    os.system('psxy region.txt -O -K -P -JM2.5i -W1.5p,red -R94/143/-12/7 >> comp3.eps')

    os.system('ps2pdf14 -dPDFSETTINGS=/prepress -dEPSCrop comp3.eps')
    os.system('pdfcrop comp3.pdf comp3.pdf')
    os.system('rm comp3.eps')
    os.system('rm region.txt')
