import os

def city_table(city_info, R, basename='comp2'):
    """Generate table of exposed cities

    Input
        city_info:
        R:
        basename: Optional basename for output pdf file
    """


    # SET GMT GENERAL PARAMETERS
    R = '-R'+str(R[0])+'/'+str(R[1])+'/'+str(R[2])+'/'+str(R[3])

    J = '-JM4.75i'
    fontsize = '9'
    font = '1'

    os.system('cat > cityinform.legend <<END'+'\n'+
    'H 13 1 Kota-kota terdampak'+'\n' +
    'D 0 1p'+'\n'+
    'N 3'+'\n'+
    'L '+ fontsize + ' '+ font +' C Kota'+'\n'+
    'L '+ fontsize + ' '+ font +' C Penduduk (x1000)'+'\n'+
    'L '+ fontsize + ' '+ font +' C Intensitas'+'\n'+
    'D 0 1p'+'\n'+
    'END')
    roman_no = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']

    # NOTE (Ole): These these must always be the same as those used in
    # the earthquake_impact_map.tex fixture
    rgb = ['255/0/255', '255/0/255', '32/159/255', '0/207/255', '85/255/255', '170/255/255', '255/240/0', '255/168/0', '255/112/0', '255/0/0'];

    N = min(len(city_info), 8)
    for i in xrange(N):

        # FIXME (Ole): Perhaps just report whole 1000's like in the table
        #if city_info['population'][i]>1000:
        #    pop = round(city_info['population'][i]/1000)
        #    pop = '%0.0f' % pop+'k'
        #else:
        #    # FIXME (Ole): pop may be unassigned here
        #    pop = '%0.0f' % pop
        pop = round(city_info['population'][i]/1000)
        pop = '%0.0f' % pop

        name = city_info['name'][i]
        color = rgb[int(city_info['intensity'][i])]
        MI = roman_no[int(round(city_info['intensity'][i]))]

        os.system('cat << END >> cityinform.legend'+'\n'+
                  'N 3'+'\n'+
                  'S 0.1i c 0.1i '+color+' 0.25p 0.2i ' +name+'\n'+
                  'L '+ fontsize + ' '+ font +' C '+pop+'\n'+
                  'L '+ fontsize + ' '+ font +' C '+MI+'\n'+
                  'D 0 1p'+'\n'+
                  'END')
    os.system('pslegend -Dx5.15i/6.0i/3.75i/1.92i/TL '+J+' '+R+' -F -K cityinform.legend > %s.eps' % basename)
    os.system('ps2pdf14 -dPDFSETTINGS=/prepress -dEPSCrop %s.eps' % basename)
    os.system('pdfcrop %s.pdf %s.pdf > logs/pdfcrop_%s.log' % (basename, basename, basename))
    os.system('rm cityinform.legend')
    os.system('rm %s.eps' % basename)
