# Extract Historical earthquakes from PAGER-CATALOGUE
# INPUTS
import numpy
import csv
import points2distance

######################FUNCTION
def list_historical_events(vec):
    lat0 = float(vec[0])
    lon0 = float(vec[1])
    list1 = [x for x in csv.reader(open('expoCat.v0.7.1.csv','r'))]
    month = ['January','February','March','April','May','June','July','August','September','October','November','December']
    intensity = ['I','II','III','IV','V','VI','VII','VIII','IX','X']
    date = []
    R =[]
    mag = []
    MI = []
    de = []
    data_tuples = []
    j =-1
    for i in range(1,len(list1)-1):
        start = ((lon0,0,0),(lat0,0,0))
        end = ((float(list1[i][9]),0,0),(float(list1[i][8]),0,0))
        r = points2distance.points2distance(start,  end)
        if r<=300:
         j = j+1
         R.insert(j,r)
         d = list1[i][2]+'/'+list1[i][3]+'/'+list1[i][4]
         date.insert(j,d)
         mag.insert(j,list1[i][11])
         MI.insert(j,list1[i][44])
         de.insert(j,list1[i][19])

         k = int(list1[i][3])-1
         mo = month[k]
         ye = list1[i][2]
         da = list1[i][4]
         dis = round(r) 
         region = list1[i][1]
         if len(region)==0:
             region = 'Indonesia'
         inten1 = intensity[int(list1[i][44])-1]
         pop1 = round(float(list1[i][41])/1000)*1000
         inten2 = intensity[int(list1[i][44])-2]
         pop2 = round(float(list1[i][40])/1000)*1000
         if (list1[i][19]=='NaN'):
            fatal_txt = '.'
         else:
            fatal_txt = ', resulting in '+list1[i][19]+' fatalities.'
                 
         data_tuples += [(d,dis,list1[i][11],list1[i][44],list1[i][19],ye,mo,da,region,inten1,pop1,inten2,pop2,fatal_txt)]

         
    dtype = [('date', 'S10'), ('distance','S10'),('magnitude','S10'),('intensity',float),('deaths','S10'),('year','S10'),('month','S10'),('day','S10'),('region','S60'),('intens1','S10'),('pop1','S20'),('intens2','S10'),('pop2','S20'),('fatal_txt','S50')]
    eve_inform = numpy.array(data_tuples,dtype=dtype)

    eve_inform = numpy.sort(eve_inform,order = ['intensity','date'])
    eve_inform = eve_inform[::-1]
    eve_inform = eve_inform[:3]
    return eve_inform

   
    

