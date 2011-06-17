import pickle
import numpy as np
##ls = np.loadtxt('landscan.asc',dtype='float',skiprows=6)

w_bound = 94.972335
s_bound = -11.009721
dl = 0.0083333333333333
ncols = 5525
nrows = 2050
e_bound = w_bound + ncols*dl
n_bound = s_bound + nrows*dl
landscan_info = {'w_bound': w_bound,'s_bound': s_bound,'e_bound': e_bound,\
                 'n_bound': n_bound,'step': dl}

##output1 = open('landscan_binary.pkl','wb')
##pickle.dump(ls, output1)
##output1.close()

output2 = open('landscan_info.pkl','wb')
pickle.dump(landscan_info, output2)

output2.close()
