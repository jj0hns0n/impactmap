import os

def exposure(expo, path, R, basename='comp4'):
    """

    Input
        expo:
        path:
        R:
        name: Optional basename for generated pdf file
    """

    R = '-R'+str(R[0])+'/'+str(R[1])+'/'+str(R[2])+'/'+str(R[3])
    J = "-JM4.75i"
    mi_scale_cpt = path +'/palettes/mi_scale.cpt'
    roman = ['II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX','X']
    pop=range(9)
    k = -1
    for i in roman:
        k = k+1

        if expo[i]>1000:
          pop[k]= round(expo[i]/1000)

          pop[k]= "%0.0f"%pop[k]+'k'

        else:
          pop[k] = "%0.0f"%expo[i]
    print pop
    font = '1'
    fontsize = '9'
    os.system('cat > pager.legend <<END'+'\n'+
    'H 16 1 Estimated population exposed to different shaking levels'+'\n' +
    'D 0 1p'+'\n'+
    'N 9'+'\n'+
    'V 0 1p'+'\n'+
    'L '+ fontsize + ' '+ font +' C MMI'+'\n'+
    'L '+ fontsize + ' '+ font +' C II'+'\n'+
    'L '+ fontsize + ' '+ font +' C III'+'\n'+
    'L '+ fontsize + ' '+ font +' C IV'+'\n'+
    'L '+ fontsize + ' '+ font +' C V'+'\n'+
    'L '+ fontsize + ' '+ font +' C VI'+'\n'+
    'L '+ fontsize + ' '+ font +' C VII'+'\n'+
    'L '+ fontsize + ' '+ font +' C VIII'+'\n'+
    'L '+ fontsize + ' '+ font +' C IX'+'\n'+
    'V 0 1p'+'\n'+
    'D 0 1p'+'\n'+
    'N 9'+'\n'+
    'V 0 1p'+'\n'+
    'L '+ fontsize + ' '+ font +' C Estimated'+'\n'+
    'L '+ fontsize + ' '+ font +' TC '+pop[0]+'\n'+
    'L '+ fontsize + ' '+ font +' TC '+pop[1]+'\n'+
    'L '+ fontsize + ' '+ font +' TC '+pop[2]+'\n'+
    'L '+ fontsize + ' '+ font +' TC '+pop[3]+'\n'+
    'L '+ fontsize + ' '+ font +' TC '+pop[4]+'\n'+
    'L '+ fontsize + ' '+ font +' TC '+pop[5]+'\n'+
    'L '+ fontsize + ' '+ font +' TC '+pop[6]+'\n'+
    'L '+ fontsize + ' '+ font +' TC '+pop[7]+'\n'+
    'G 0.000i'+'\n'+
    'L '+ fontsize + ' '+ font +' C Population'+'\n'+
    'V 0 1p'+'\n'+
    'END')
    os.system('psscale -D3.88i/6.652i/6.2i/0.2ih -C'+mi_scale_cpt + ' -B0/0  -K -S  > %s.eps' % basename)
    os.system('pslegend -Dx3.5i/7.0i/7i/0.95i/TC '+J+' '+R+' -O -F -K pager.legend  >> %s.eps' % basename)
    os.system('ps2pdf14 -dPDFSETTINGS=/prepress -dEPSCrop %s.eps' % basename)
    os.system('pdfcrop %s.pdf %s.pdf' % (basename, basename))
    os.system('rm pager.legend')
    os.system('rm %s.eps' % basename)
