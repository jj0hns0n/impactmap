# Plot the region map
import os
import numpy as np
def region_map(event_info,A,R,shakedata_dir,library_dir):

    # SET PATHS
    mi_xyz = shakedata_dir+'/grid.xyz'
    mi_cpt = library_dir+'/palettes/mi.cpt'
    pop_grd = library_dir+'/population/landscan2008.grd'
    pop_cpt = library_dir+'/palettes/pop.cpt'


    step = np.abs(A[0,0]-A[1,0])*60

    #SET GMT GENERAL PARAMETERS
    R = '-R'+str(R[0])+'/'+str(R[1])+'/'+str(R[2])+'/'+str(R[3])
    I_mi = '-I'+str(step)+'m'
    B = "-Ba120mf120mwSEn"
    J = "-JM4.75i"

    # Convert the 'grid.xyz" to GMT '.grd' file
    os.system('awk '+"'NR!=1 {print $1,$2,$5}' "+mi_xyz+'|xyz2grd -Gmi.grd '+I_mi+' '+R)

    os.system('psbasemap '+R+' '+J+' -K -P '+B+'  > comp1.eps')
    os.system('grdimage '+pop_grd+' -C'+pop_cpt+' '+R+' '+J+' -K -P -O >> comp1.eps')
    os.system('pscoast '+R+' '+J+' -K -P -O  -Df -W -S192/216/255 >> comp1.eps')
    os.system ('grdcontour mi.grd -C'+mi_cpt+' -W+1.5p '+R+' '+J+' -K -P -O >> comp1.eps')

    # plot the epicenter
    os.system('echo '+str(event_info['lon'])+' '+str(event_info['lat'])+'| psxy '+R+' '+J+' -K -P -O -Sa0.500 -Gred -W1.5,black >> comp1.eps')
    
    # plot cities 
    os.system('pstext city.txt -J -R -O -K -Gblack>> comp1.eps')
              
    os.system('ps2pdf14 -dPDFSETTINGS=/prepress -dEPSCrop comp1.eps')
    os.system('pdfcrop comp1.pdf comp1.pdf')
    os.system('rm mi.grd')
    os.system('rm city.txt')
    os.system('rm *.eps')
    os.system('cp comp1.pdf ~/')

    


##from event_info import event_info
##import numpy as np
##import pickle
##shakedata_dir = os.environ['SHAKEDATA']
##library_dir = os.environ['IMPACTLIB']
##mi_cpt = os.path.join(library_dir, 'palettes', 'mi.cpt')
##event_info,A = event_info(shakedata_dir)
##path = library_dir
##pkl_file = open(path+'/population/landscan_binary.pkl','r')
##ls = pickle.load(pkl_file)
##ls = np.flipud(ls)
##pkl_file.close()
##pkl_file = open(path+'/population/landscan_info.pkl','r')
##ls_info = pickle.load(pkl_file)
##pkl_file.close()
##
##R = np.zeros(4,dtype = float)
##R[0] = np.maximum(float(event_info['w_bound']),ls_info['w_bound'])
##R[1] = np.minimum(float(event_info['e_bound']),ls_info['e_bound'])
##R[2] = np.maximum(float(event_info['s_bound']),ls_info['s_bound'])
##R[3] = np.minimum(float(event_info['n_bound']),ls_info['n_bound'])
##
##step = np.abs(A[0,0]-A[1,0])*60
##
##R = '-R'+str(R[0])+'/'+str(R[1])+'/'+str(R[2])+'/'+str(R[3])
##I_mi = '-I'+str(step)+'m'
##B = "-Ba120mf120mwSEn"
##J = "-JM4.75i"
##
##os.system('awk '+"'NR!=1 {print $1,$2,$5}' ../../shakedata/grid.xyz|xyz2grd -Gmi.grd"+' '+I_mi+' '+R)

##os.system('psbasemap -X5 -Y10 '+R+' '+J+' -K -P '+B+'  > comp1.eps')
##os.system('grdimage ../../impactlib/population/landscan2008.grd -C../../impactlib/palettes/pop.cpt '+R+' '+J+' -K -P -O >> comp1.eps')
##os.system('pscoast '+R+' '+J+' -K -P -O  -Df -W -S192/216/255 >> comp1.eps')
##os.system ('grdcontour mi.grd -C../../impactlib/palettes/mi.cpt -W+1.5p '+R+' '+J+' -K -P -O >> comp1.eps')
##os.system('ps2pdf14 -dPDFSETTINGS=/prepress -dEPSCrop comp1.eps')
##os.system('pdfcrop comp1.pdf comp1.pdf')

 

