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
            start = ((float(A[b][0]),0,0),(float(A[b][1]),0,0))
            end = ((float(A[T[i]][0]),0,0),(float(A[T[i]][1]),0,0))
            #print start
            #print end
            r = points2distance.points2distance(start,end)
            if r>=dis_lim:
                T2 += [(T[i])]
                
        #print T2
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

    for i in index:
        #print A[i][4]
        os.system('cat << END >> city.txt'+'\n'+
        ''+A[i][0]+' '+A[i][1]+' 15 5 4 2 '+A[i][4]+'\n'+
        'END')
        
        
           
        
    
    
