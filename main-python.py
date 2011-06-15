import scipy as sp
from matplotlib.mlab import griddata
import numpy as np
import pickle
import os

filename = 'java_2011.xyz'
xls_corner = 94.97233;5
yls_corner = -11.009721;
dl = 0.0083333333333333;
ncols = 5525;
nrows = 2050;
##ls = np.loadtxt('landscan.asc',dtype='float',skiprows=6)
pkl_file = open('landscan_binary.pkl','r')
ls = pickle.load(pkl_file)
ls = np.flipud(ls)
pkl_file.close()

cond = "'{if (NR==1) print $10,$12,$11,$13}'"
os.system ('awk '+cond+' '+filename+' > mi_header_tmp.txt')
R = np.loadtxt('mi_header_tmp.txt')
col_low = np.abs(R[0]-xls_corner)/dl;
col_low = np.ceil(col_low);
col_high = np.abs(R[1]-xls_corner)/dl;
col_high = np.floor(col_high);
row_low = np.abs(R[2]-yls_corner)/dl;
row_low = np.ceil(row_low);
row_high = np.abs(R[3]-yls_corner)/dl;
row_high = np.floor(row_high);
##print col_low,col_high,row_low,row_high # CHECK POINT: PASSED
x_min = col_low*dl+xls_corner;
x_max = col_high*dl+xls_corner;
y_min = row_low*dl+yls_corner;
y_max = row_high*dl+yls_corner;
##print x_min,y_min,x_max,y_max  # CHECK POINT: PASSED

x = np.arange(x_min,x_max+dl,dl)#x_min:dl:x_max;
##print np.min(x),np.max(x),np.size(x) # CHECK POINT: PASSED
y = np.arange(y_min,y_max+dl,dl)#y_min:dl:y_max;
##print np.min(y),np.max(y),np.size(y) # CHECK POINT: PASSED
[X,Y] = np.meshgrid(x,y)
##print X[50,37],Y[60,43] # CHECK POINT: PASSED

# Note that in Python indexing starts from 0!
Z_pop = ls[row_low-1:row_high][:,col_low-1:col_high]
##print np.min(np.min(Z_pop)),np.max(np.max(Z_pop)),np.shape(Z_pop) # CHECK POINT: PASSED
Z_pop[Z_pop==-9999]= np.NaN
##print np.min(np.nanmin(Z_pop)),np.max(np.nanmax(Z_pop)),np.shape(Z_pop) # CHECK POINT: PASSED
##print Z_pop[158,707] # CHECK POINT: PASSED

cond = "'{if (NR!=1) print $1,$2,$5}'"
os.system ('awk '+cond+' '+filename+' > mi_tmp.txt')
A = np.loadtxt('mi_tmp.txt')
lon = A[:,0]
lat = A[:,1]
mi = A[:,2]

dl = lon[1]-lon[0]
ncol = np.size(np.arange(np.min(lon),np.max(lon),dl))
nrow = np.size(np.arange(np.min(lat),np.max(lat),dl))
col = np.arange(np.min(lon),np.max(lon),dl)
row = np.arange(np.min(lat),np.max(lat),dl)
##print dl,ncol,nrow,col,row # CHECK POINT: PASSED
X1_mi = lon.reshape(nrow,ncol)
Y1_mi = lat.reshape(nrow,ncol)
Z1_mi = mi.reshape(nrow,ncol)
##print np.shape(Z1_mi),Z1_mi[0,0],Z1_mi[-1,-1],Z1_mi[65,51] # CHECK POINT: PASSED
##print np.shape(X1_mi),X1_mi[0,0],X1_mi[-1,-1],X1_mi[65,51] # CHECK POINT: PASSED


############# 2D Interpolation########################
points = A[:,0:2]
print np.shape(points),np.shape(A),points[100,:]
values = A[:,2]
print np.shape(values),values[100]
##X1_mi = X1_mi.reshape(nrow*ncol).T
##Y1_mi = X1_mi.reshape(nrow*ncol).T
##Z1_mi = Z1_mi.reshape(nrow*ncol).T
##print np.shape(X1_mi),len(Y1_mi),np.shape(Z1_mi)
##X =  X.reshape(np.size(X))
##Y =  Y.reshape(np.size(Y))
##Z_I = griddata(col,row,Z1_mi,X,Y)





##spl = interpolate.RectBivariateSpline(np.flipud(Y1_mi[:,0]),X1_mi[0,:],Z1_mi, kx=1, ky=1, s=0)
####print spl
######xi = X[1,:]
######yi = Y[:,1]
##Z_I = spl(y,x)
##print np.min(Z_I),np.max(Z_I),np.shape(Z_I),np.shape(Z_pop)
####print np.shape(Z_I),np.shape(Z_pop)
####f = np.nonzero((Z_I<5.5) & (Z_I>=4.5))
####print len(f)
##pop_expo = np.sum(np.nansum(Z_pop[(Z_I<5.5) & (Z_I>=4.5)]))
##print Z_pop[(Z_I<5.5) & (Z_I>=4.5)]
