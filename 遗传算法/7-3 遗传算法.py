# -*- coding: utf-8 -*-

from scipy.optimize import minimize
 
f = lambda x: -(x[0]**2*x[1]*x[2]**2/
               (2*x[0]**3*x[2]**2+3*x[0]**2*x[1]**2+
               2*x[1]**2*x[2]**2+x[0]**2*x[1]**2*x[2]**2))

cons = ({'type': 'ineq', 'fun': lambda x:  x[0]**2+x[1]**2+x[2]**2-1},
         {'type': 'ineq', 'fun': lambda x: -x[0]**2-x[1]**2-x[2]**2+4})

res = minimize(f, (1,1,1), method='SLSQP', constraints=cons)
print(res)