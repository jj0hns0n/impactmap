# Plot the region map
import os
import numpy as np
def region_map(event_info, A, R,
               shakedata_dir, event_name, library_dir, basename='comp1'):
    """

    Input
        event_info:
        A:
        R:
        shakedata_dir:
        library_dir:
        basename: Optional basename for the oupte pdf file

    Output:
        Pdf file using given name showing the exposure map
    """

    path = os.path.join(shakedata_dir, event_name, 'output', 'grid.xyz')

    # SET PATHS
    mi_xyz = os.path.join(shakedata_dir, event_name, 'output', 'grid.xyz')
    mi_cpt = library_dir+'/palettes/mi.cpt'
    pop_grd = library_dir+'/population/landscan2008.grd'
    pop_cpt = library_dir+'/palettes/pop.cpt'


    step = np.abs(A[0,0]-A[1,0])*60

    #SET GMT GENERAL PARAMETERS
    R = '-R'+str(R[0])+'/'+str(R[1])+'/'+str(R[2])+'/'+str(R[3])
    I_mi = '-I'+str(step)+'m'
    B = '-Ba120mf120mwSEn'
    J = '-JM4.75i'

    # Convert the 'grid.xyz" to GMT '.grd' file
    os.system('awk '+"'NR!=1 {print $1,$2,$5}' "+mi_xyz+'|xyz2grd -Gmi.grd '+I_mi+' '+R)

    os.system('psbasemap '+R+' '+J+' -K -P '+B+'  > %s.eps' % basename)
    os.system('grdimage '+pop_grd+' -C'+pop_cpt+' '+R+' '+J+' -K -P -O >> %s.eps' % basename)
    os.system('pscoast '+R+' '+J+' -K -P -O  -Df -W -S192/216/255 >> %s.eps' % basename)
    os.system ('grdcontour mi.grd -C'+mi_cpt+' -W+1.5p '+R+' '+J+' -K -P -O >> %s.eps' % basename)

    # plot the epicenter
    os.system('echo '+str(event_info['lon'])+' '+str(event_info['lat'])+'| psxy '+R+' '+J+' -K -P -O -Sa0.500 -Gred -W1.5,black >> %s.eps' % basename)

    # plot cities
    os.system('pstext city.txt -J -R -O -K -Gblack>> %s.eps' % basename)

    # Generate map as pdf cropped to bounding box
    os.system('ps2pdf14 -dPDFSETTINGS=/prepress -dEPSCrop %s.eps' % basename)
    os.system('pdfcrop %s.pdf %s.pdf' % (basename, basename))
    os.system('/bin/rm mi.grd')
    os.system('/bin/rm city.txt')
    os.system('/bin/rm *.eps')

    # FIXME (Ole): I don't think we need this
    os.system('cp %s.pdf ~/' % basename)



