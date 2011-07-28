import numpy as np
import scipy.stats as dist
def fatality(pop_expo):
    teta = 13.2488
    beta = 0.1508
    zeta = 1.641

    I = np.arange(5,11,dtype = 'float')
    Pop = np.array([pop_expo['V'],pop_expo['VI'],pop_expo['VII'],\
                    pop_expo['VIII'],pop_expo['IX'],pop_expo['X']])

    X = (1/beta)*np.log(I/teta)
    nu = dist.norm.cdf(X)

    mu = np.sum(nu*Pop);
    mu = np.log(mu);

    P = np.zeros(7,dtype='float')
    a = np.array([1, 10, 100, 1000,  10000],dtype = 'float')
    b = np.array([9, 99, 999, 10000, 100000],dtype = 'float')
    P[0] = dist.norm.cdf((np.log(a[0])-mu)/zeta)
    P[1:6] = dist.norm.cdf((np.log(b)-mu)/zeta) - dist.norm.cdf((np.log(a)-mu)/zeta)
    P[6] = 1-np.sum(P[0:6])

    ranges = ['<1','1-10','10-100','100-1000','1000-10000','10000-100000','>100000']
    P = P*100
    Prob = dict(zip(ranges,P))
    return Prob

    
