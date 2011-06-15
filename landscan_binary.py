import pickle
import numpy as np
ls = np.loadtxt('landscan.asc',dtype='float',skiprows=6)
output = open('landscan_binary.pkl','wb')
pickle.dump(ls, output)
