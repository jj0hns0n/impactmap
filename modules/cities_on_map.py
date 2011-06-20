import numpy
import points2distance
import os

#########################
def cities_on_map(A,dis_lim):
    index = [0]
    T = range(1,len(A))
    T2 = []
    b = 0
    n = -1
    while n < 0:
        for i in range(len(T)):
            start = ((A['lat'][b],0,0),(A['lon'][b],0,0))
            end = ((A['lat'][T[i]],0,0),(A['lon'][T[i]],0,0))
            r = points2distance.points2distance(start,end)
            if r>=dis_lim:
                T2 += [(T[i])]

        if len(T2)>1:
            index += [(T2[0])]
            b = T2[0]
            T = T2[1:]
            T2 = []
        elif len(T2)==1:
            index += [(T2[0])]
            n = 100
        else:
            n = 100

    print A['lat']
    print len(A['lat'])
    print index, len(index)
    for i in index:
        os.system('cat << END >> city.txt'+'\n'+
        ''+str(A['lat'][i])+' '+str(A['lon'][i])+' 15 5 4 2 '+A['name'][i]+'\n'+
        'END')






