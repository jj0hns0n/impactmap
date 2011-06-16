import os
import numpy
import sys
import scipy
from scipy.io import netcdf_file as netcdf
import scipy.stats as dist
from xml.dom import minidom
import list_historical_events
import cities_on_map
event = sys.argv[1]

shakedata_dir = os.environ['SHAKEDATA']
library_dir = os.environ['IMPACTLIB']

pop_file = os.path.join(library_dir, 'population', 'landscan2008.grd')
images_path = os.path.join(library_dir, 'images')
mi_cpt = os.path.join(library_dir, 'palettes', 'mi.cpt')
mi_scale_cpt = os.path.join(library_dir, 'palettes', 'mi_scale.cpt')

output_path = os.path.join(shakedata_dir, event, 'output')
mmi_file = os.path.join(output_path, 'mi.grd')
foutfile = os.path.join(output_path, 'event_footprint.txt')

cities_file = os.path.join(library_dir, 'cities', 'Indonesia.txt')
topo_grd = os.path.join(library_dir, 'topography', 'Indonesia.topobath.1m.grd')
topo_grad = os.path.join(library_dir, 'topography', 'topo_grad.grd')

event_path = os.path.join(shakedata_dir, event, 'input')
disclaimer = os.path.join(event_path, event + '.disclaimer.txt')
event_xml = os.path.join(event_path, 'event.xml')

##############################################################################
# GET EVENT INFORMATION
print 'GET EVENT INFORMATION'
xmldoc = minidom.parse(event_xml)
event = xmldoc.getElementsByTagName('earthquake')
event = event[0]
mag_eve = event.attributes["mag"].value.encode('US-ASCII')
loc_eve = event.attributes["locstring"].value.encode('US-ASCII')
lon_eve = event.attributes["lon"].value.encode('US-ASCII')
lat_eve = event.attributes["lat"].value.encode('US-ASCII')
dep_eve = event.attributes["depth"].value.encode('US-ASCII')
gen_eve = 'M'+mag_eve+ '  '+loc_eve
info_eve = 'Latitude: '+lat_eve+ '@~\260@~ Longitude: '+lon_eve+'@~\260@~  Depth: '+dep_eve + 'km'
ot_eve = event.attributes["year"].value.encode('US-ASCII')+'-'+event.attributes["month"].value.encode('US-ASCII') \
         + '-' + event.attributes["day"].value.encode('US-ASCII')+'  '+ event.attributes["hour"].value.encode('US-ASCII') \
         +':'+event.attributes["minute"].value.encode('US-ASCII')+':'+ event.attributes["second"].value.encode('US-ASCII')
##############################################################################
# Copy MMI GRID AND GET MMI GRID SIZE
print 'GET MMI GRID SIZE'
os.system('cp '+mmi_file+' .')
#os.system('grdsample '+mmi_file+' -Gmi.grd -T -I30c')
x = netcdf('mi.grd','r').variables['lon'][::-1]
y = netcdf('mi.grd','r').variables['lat'][::-1]
x_min = float(numpy.min(x))
x_max = float(numpy.max(x))
y_min = float(numpy.min(y))
y_max = float(numpy.max(y))
#os.system('cp '+mmi_file+' .')
################################################################################
# SET FINAL MAP EXTENDS
print 'GET POPULATION GRID SIZE'
x = netcdf(pop_file,'r').variables['x'][::-1]
y = netcdf(pop_file,'r').variables['y'][::-1]
x_min_pop = float(numpy.min(x))
x_max_pop = float(numpy.max(x))
y_min_pop = float(numpy.min(y))
y_max_pop = float(numpy.max(y))
print 'SET MAP EXTENDS'
x_min = numpy.maximum(x_min,x_min_pop)
x_max = numpy.minimum(x_max,x_max_pop)
y_min = numpy.maximum(y_min,y_min_pop)
y_max = numpy.minimum(y_max,y_max_pop)
footprint = str(x_min) + '\t' + str(y_max) + '\n'
footprint = footprint + str(x_max) + '\t' + str(y_max) + '\n'
footprint = footprint + str(x_max) + '\t' + str(y_min) + '\n'
footprint = footprint + str(x_min) + '\t' + str(y_min) + '\n'
footprint = footprint + str(x_min) + '\t' + str(y_max)
footprint_file = open(foutfile,'w')
footprint_file.write(footprint)
footprint_file.close()
################################################################################
# SET GMT VARIABLES
os.system('gmtset ANNOT_FONT_SIZE_PRIMARY 9p ANNOT_FONT_PRIMARY 1')
B = "-Ba120mf120mwSEn"
R = '-R'+str(x_min)+'/'+str(x_max)+'/'+str(y_min)+'/'+str(y_max)
LF = "-Lfx0.0/1.0/.0/200"
J = "-JQ4.75i"
S = R+' '+J+' -K -P -V'
M = R+' '+J+' -O -K -P'
fontsize ='9'
fontsizeHeading ='16'
font = '1'
fontHeading ='1'
shore_color="10/40/100"
water_color="120/160/220"
os.system('gmtset ANNOT_OFFSET_PRIMARY = 0.15c PLOT_DEGREE_FORMAT ddd:mm:ss')
os.system('gmtset BASEMAP_TYPE = plain')
ps = './pop_expo.ps'
##################################################################################
# GRDCUT POPULATION DATA
# make zero grd
os.system('grdmath -I30c -F '+R+' 1 0 MUL = tmp_zero.grd');
# remove NaNs from population grd
os.system('grdsample '+pop_file+' -Gtmp_pop.grd '+R)
os.system('grdmath tmp_pop.grd tmp_zero.grd MAX = tmp_pop.grd');
###########################################################################################################
# GET POPULATION AT DIFFERENT MMI LEVELS
print 'GET POPULATION AT DIFFERENT MMI LEVELS'
os.system('grdsample mi.grd -Gmi_tmp.grd -T -I30c')
os.system('grdsample mi_tmp.grd -Gmi_tmp.grd '+R)
mmi_inc = 1.0
mmi_inc_half = mmi_inc / 2
mmi_range = numpy.arange(2,10,mmi_inc)
pop = numpy.zeros([1,8])
fatal = numpy.zeros([1,8])
fatal50 = numpy.zeros([1,8])
fatal25 = numpy.zeros([1,8])
fatal75 = numpy.zeros([1,8])
data_tuples = []
i = -1
for mmi in mmi_range:
    # get cells > MMI
    x = mmi - mmi_inc_half
    os.system('grdmath mi_tmp.grd '+str(mmi - mmi_inc_half)+' GT = tmp1.grd')
    # get cells <= MMI
    os.system('grdmath mi_tmp.grd '+str(mmi + mmi_inc_half)+' LE = tmp2.grd')
    # multiply tmp grids to get valid MMI cells
    os.system('grdmath tmp1.grd tmp2.grd MUL = tmp.grd')
    # get total population exposed to MMI
    os.system('grdmath tmp.grd tmp_pop.grd MUL = tmp.grd')
    x = netcdf('tmp.grd','r').variables['z'][::-1]
    total_pop = int(round(numpy.sum(x)))
    teta = 14.05
    beta = 0.17
    zeta = 2.15
    fatal_rate = dist.norm.cdf(1/beta*scipy.log(mmi/teta))
    pop = total_pop
    fatal = round(fatal_rate*total_pop)
    i = i+1
    fatal50[0][i] = numpy.exp(zeta*dist.norm.ppf(0.5)+ numpy.log(fatal))
    fatal25[0][i] = numpy.exp(zeta*dist.norm.ppf(0.25)+ numpy.log(fatal))
    fatal75[0][i] = numpy.exp(zeta*dist.norm.ppf(0.75)+ numpy.log(fatal))
    fatal = "%0.0f"%fatal
    if pop>1000:
      pop = round(pop/1000)
      pop = "%0.0f"%pop+'k'
    else:
      pop = "%0.0f"%pop
    data_tuples += [(pop,fatal)];
dtype = [('population', 'S10'), ('fatalities','S10')]
pager_data = numpy.array(data_tuples,dtype=dtype)
fatal25 = "%0.0f"%round(sum(fatal25[0]))
fatal75 = "%0.0f"%round(sum(fatal75[0]))
##################################################################################
# GET LIST OF THE CITIES, CALCULATE INTENSITIES AND SORT BASED ON INTENSITY
print 'GET LIST OF THE CITIES, CALCULATE INTENSITIES AND SORT BASED ON INTENSITY'
os.system('grdtrack ' + cities_file + ' -Gmi_tmp.grd>table.txt')
data = open('table.txt').readlines()

data_tuples = []
roman_no = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
rgb = ['255/0/255','255/0/255','32/159/255', '0/207/255', '85/255/255', '170/255/255', '255/240/0', '255/168/0', '255/112/0', '255/0/0'];
i = -1;
for line in data:
  i = i +1
  data2 = data[i].split('\t')

  lon = float(data2[0])
  lat = float(data2[1])
  pop = int(data2[2])
  city = data2[3]

  data4 = data2[4].split("\n")
  mmi = float(data4[0])
  if pop>1000:
      pop_int = round(pop/1000)
      pop = "%0.0f"%pop_int+'k'
  else:
      pop = "%0.0f"%pop
  a = round(mmi)
  MMI = roman_no[int(a)]
  RGB = rgb[int(a)]
  data_tuples += [(lon,lat,pop,mmi,city,MMI,RGB,pop_int,a)];
dtype = [('longitude', 'S10'), ('latitude','S10'),('population','S10'),('intensity',float),('name','S10'),('MMI','S10'),('RGB','S10'),('pop_int',float),('intens',int)]
city_inform = numpy.array(data_tuples,dtype=dtype)
city_inform = numpy.sort(city_inform,order = ['intens','pop_int'])
city_inform = city_inform[::-1]
city_inform = city_inform[:8]
cities_on_map.cities_on_map(city_inform,50)
################################################################################
# GET HISTORICAL EVENTS WITHIN 300 KM OF THIS EVENT
print 'GET HISTORICAL EVENTS WITHIN 300 KM OF THIS EVENT'
vec = (lat_eve,lon_eve)
hist_eve = list_historical_events.list_historical_events(vec)

################################################################################
print 'PLOT POPULATION GRID, MMI GRID, CITIES LOCATION AND EPICENTER'
# SMOOTH MMI GRID
##os.system('grdmath mi.grd 10 MUL = mi.grd')
##os.system('grdmath mi.grd CEIL = mi.grd')
##os.system('grdmath mi.grd 10 DIV = mi_smooth.grd')
#os.system('grdsample mi.grd -Gmi_tmp.grd -T -I30c')
os.system('grd2xyz mi_tmp.grd > mi.xyz')
os.system('blockmedian mi.xyz -I3m '+R+' > mi_smooth.xyz')
os.system('surface mi_smooth.xyz -Gmi_smooth.grd -I30c -T0 -C0.0001  '+R)
################################################################################
# PLOT  POPULATION AND MMI GRID
os.system('psbasemap  -X0.5 -Y8.5 '+R+' '+J+' -K -P '+B+'  > '+ps)
os.system('grdimage tmp_pop.grd -C'+output_path+'/pop.cpt '+M+' >> '+ps)
os.system('makecpt -Cno_green -T2/9.0/1  > ' + mi_cpt)
os.system('grdcontour mi_smooth.grd -C'+mi_cpt+' -W+2p '+M+' -Q100 -A-   >> '+ps)
os.system('pscoast '+M+' -Df -W -S192/216/255 >> '+ps)
os.system('grdcontour mi_smooth.grd -C'+output_path+'/poptest.cpt -W+2p,- '+M+' -Q100 -A- >> '+ps)
################################################################################
# PLOT EPICENTER AND CITIES on MAP
os.system('echo '+lon_eve+' '+lat_eve+'| psxy '+M+' -Sa0.500 -Gred -W1.5,black  >> '+ps)
##j = -1
##for i in city_inform:
##    j = j+1
##    a = city_inform[j][0]
##    b = city_inform[j][1]
####    a = "%0.2f"%a
####    b = "%0.2f"%b
##    os.system('echo '+a+' '+b+'| psxy '+M+' -Ss0.300 -Gblack -W1.0,red >> '+ps)
################################################################################
# PLOT CITIES ON THE MAP
os.system('pstext city.txt -J -R -O -K -Gblack>> '+ps)
################################################################################
# PLOT  MINI INDONESIA
os.system('makecpt -Crelief -T-9200/9200/100 -Z  > releif.cpt')
os.system('psbasemap -R94/143/-12/7 -JM2.5i -K -O -P -X-0.01 -Y-3.2 -Gwhite >> '+ps)
os.system('grdimage '+ topo_grd +' -I' + topo_grad + ' -B10d -R94/141.5/-11.5/6 -K -O -JM2.5i -Creleif.cpt >>'+ps)
os.system('psxy ' + foutfile + ' -O -K -P -JM2.5i -W1.5p,red -R94/143/-12/7 >> '+ps)

# PLOT THE LEGENDS
print 'PLOT THE LEGENDS'
#LEGEND ONE
os.system('cat > event.legend <<END'+'\n'+
'L ' + fontsizeHeading + ' ' + fontHeading + ' L '+gen_eve+'\n'+
'L ' + fontsizeHeading + ' ' + fontHeading + ' L '+ot_eve+'\n'+
'L ' + fontsizeHeading + ' ' + fontHeading + ' L '+info_eve+'\n'+
'END')
os.system('pslegend -Dx0.0i/8i/6i/0.8i/TL -J -R -O  -K event.legend >> '+ps)
#LEGEND TWO
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
'L '+ fontsize + ' '+ font +' TC '+pager_data[0][0]+'\n'+
'L '+ fontsize + ' '+ font +' TC '+pager_data[1][0]+'\n'+
'L '+ fontsize + ' '+ font +' TC '+pager_data[2][0]+'\n'+
'L '+ fontsize + ' '+ font +' TC '+pager_data[3][0]+'\n'+
'L '+ fontsize + ' '+ font +' TC '+pager_data[4][0]+'\n'+
'L '+ fontsize + ' '+ font +' TC '+pager_data[5][0]+'\n'+
'L '+ fontsize + ' '+ font +' TC '+pager_data[6][0]+'\n'+
'L '+ fontsize + ' '+ font +' TC '+pager_data[7][0]+'\n'+
'G 0.000i'+'\n'+
'L '+ fontsize + ' '+ font +' C Population'+'\n'+
'V 0 1p'+'\n'+
'END')
os.system('psscale -D3.88i/6.652i/6.2i/0.2ih -C'+mi_scale_cpt + ' -B0/0 -O -K -S  >>'+ps)
os.system('pslegend -Dx3.5i/7.0i/7i/0.88i/TC -J -R -O -F -K pager.legend  >> '+ps)
#LEGEND THREE
os.system('cat > cityinform.legend <<END'+'\n'+
'H 13 1 Affected Cities'+'\n' +
'D 0 1p'+'\n'+
'N 3'+'\n'+
'L '+ fontsize + ' '+ font +' C City'+'\n'+
'L '+ fontsize + ' '+ font +' C Population'+'\n'+
'L '+ fontsize + ' '+ font +' C Intensity'+'\n'+
'D 0 1p'+'\n'+
'END')
for i in xrange(len(city_inform)):
    os.system('cat << END >> cityinform.legend'+'\n'+
              'N 3'+'\n'+

    'S 0.1i c 0.1i '+city_inform[i][6]+' 0.25p 0.2i ' +city_inform[i][4]+'\n'+

    'L '+ fontsize + ' '+ font +' C '+city_inform[i][2]+'\n'+
    'L '+ fontsize + ' '+ font +' C '+city_inform[i][5]+'\n'+

    'D 0 1p'+'\n'+
    'END')
os.system('pslegend -Dx5.15i/6.0i/2.75i/1.92i/TL -J -R -O -F -K cityinform.legend >> '+ps)
#LEGEND IV
os.system('cat > pop-legend.legend <<END'+'\n'+
'H 8 1 Population per square km'+'\n' +
'D 0 1p'+'\n'+
'N 2'+'\n'+
'S 0.3i s 0.2i 223/223/223 0.25p 0.2i \n'+
'L '+ fontsize + ' '+ font +' L 1-10 \n'+
'S 0.3i s 0.2i 159/159/159 0.25p 0.2i \n'+
'L '+ fontsize + ' '+ font +' L 10-100 \n'+
'N 2'+'\n'+
'S 0.3i s 0.2i 96/96/96 0.25p 0.2i \n'+
'L '+ fontsize + ' '+ font +' L 100-1000 \n'+
'S 0.3i s 0.2i 32/32/32 0.25p 0.2i \n'+
'L '+ fontsize + ' '+ font +' L 1000-10000 \n'+
'END')
os.system('pslegend -Dx3.2i/0.9i/1.5i/0.9i/TL -J -R -O  -K pop-legend.legend >> '+ps)
#LEGEND V
os.system('cat > fatal-rep.legend <<END'+'\n'+
'N 1'+'\n'+
'L '+ fontsize + ' '+ font +' L Based on empirical model for global fatality \n'+
'L '+ fontsize + ' '+ font +' L estimation, the numbers of casualties  \n'+
'L '+ fontsize + ' '+ font +' L associated with 25 and 75 percentiles are \n'+
'L '+ fontsize + ' '+ font +' L ' +fatal25+ ' and ' +fatal75+ ', respectively\n'+
'END')
os.system('pslegend -Dx5.15i/3.5i/2.75i/1i/TL -J -R -O -F -K fatal-rep.legend >> '+ps)
#LEGEND VI
os.system('cat > disclaimer.legend <<END'+'\n'+
'D 0 1p'+'\n'+
'N 1'+'\n'+
'L '+ fontsize + ' '+ font +' L  Users should consider the preliminary nature of this information and check for updates as additional data becomes available. \n'+
'L '+ fontsize + ' '+ font +' L  Population exposure estimates are NOT a direct estimate of earthquake damage; comparable shaking will result in significantly \n'+
'L '+ fontsize + ' '+ font +' L  lowerlosses in regions with well built structures than in regions with vulnerable structures. \n'+
'L '+ fontsize + ' '+ font +' L  A magnitude '+hist_eve[0][2]+' earthquake '+hist_eve[0][1]+' km from the current event struck the '+hist_eve[0][8]+' region on '+hist_eve[0][6]+' '+hist_eve[0][7]+', '+hist_eve[0][5]+' (UTC), \n'+
'L '+ fontsize + ' '+ font +' L  with estimated population exposures of '+hist_eve[0][10]+' at intensity '+hist_eve[0][9]+' and '+hist_eve[0][12]+' at intensity '+hist_eve[0][11]+''+hist_eve[0][13]+' \n'+
'L '+ fontsize + ' '+ font +' L  In addition, a magnitude '+hist_eve[1][2]+' earthquake '+hist_eve[1][1]+' km from the current event struck the '+hist_eve[1][8]+' region on '+hist_eve[1][6]+' '+hist_eve[1][7]+', '+hist_eve[1][5]+' (UTC), \n'+
'L '+ fontsize + ' '+ font +' L  with estimated population exposures of '+hist_eve[1][10]+' at intensity '+hist_eve[1][9]+' and '+hist_eve[1][12]+' at intensity '+hist_eve[1][11]+''+hist_eve[1][13]+' \n'+
'L '+ fontsize + ' '+ font +' L  Recent earthquakes in this area have also triggered landslide and tsunami hazards that have contributed to losses. \n'+
'L '+ fontsize + ' '+ font +' L  Shaking intensities are calculated by BMKG using USGS ShakeMap methodology. \n'+
'L '+ fontsize + ' '+ font +' L  Population data are estimated from Oak Ridge Laoratorys LandScan 2006 Global Population Database. \n'+
'L '+ fontsize + ' '+ font +' L  Figures are produced using Generic Mapping Tools (http://gmt.soest.hawaii.edu/). \n'+
'END')
os.system('pslegend -Dx0i/-0.2i/8i/5i/TL -J -R -O  -K disclaimer.legend >> '+ps)

# PLOT THE LOGO
os.system('psimage ' + images_path + '/LOGO_BMKG.ras -K -P -O -W0.5i -Y21.35 -X0.7i -Gtwhite >> '+ps)
os.system('psimage ' + images_path + '/AIFDR_ALL_COLOR.ras -K -P -O -W2.5i -X5.0 -Y-1.2 >> '+ps)
os.system('psimage ' + images_path + '/BNBP_greenboarder.ras -K -P -O -W0.8i -X9.8 -Y1 >> '+ps)

os.system('rm *.grd *.legend *.xyz *.cpt *.txt')
