# -*- coding: utf-8 -*-

import numpy as np

np.random.seed(210)

f = lambda x: (x[0]**2*x[1]*x[2]**2/
               (2*x[0]**3*x[2]**2+3*x[0]**2*x[1]**2+
               2*x[1]**2*x[2]**2+x[0]**2*x[1]**2*x[2]**2))

st = lambda x: 1<=(x**2).sum()<=4

NP = 30
NG = 150
a = 0.05
fit = lambda i: a*(1-a)**i
q = np.cumsum([fit(i) for i in range(NP)])
Pc = 0.2
Pm = 0.04
c = 0.6

x = np.zeros((NP,3))
for i in range(NP):
    x[i] = np.random.random(3)*2
    while not (st(x[i])):
        x[i] = np.random.random(3)*2
nx = x.copy()

v0 = [0,0,0]
f0 = 0
for i in range(NG):
    fx = np.array([f(x[i]) for i in range(NP)])
    idx = np.argsort(-fx)
    x = x[idx]
    fx = fx[idx]
    # 保留最佳个体
    if f0 < fx[0]:
        v0 = x[0]
        f0 = fx[0]
        print(f0)
    
    # 轮盘赌
    for j in range(NP):
        nx[j] = x[-1]
        r = np.random.random()*q[-1]
        for k in range(NP):
            if r < q[k]:
                nx[j] = x[k]
                break

    x = nx.copy()

    # 交叉
    np.random.shuffle(nx)
    for j in np.arange(0,NP,2):
        r = np.random.random()
        if r <= Pc:
            x[j] = c*nx[j]+(1-c)*nx[j+1]
            x[j+1] = c*nx[j+1]+(1-c)*nx[j]
            if not st(x[j]) or not st(x[j+1]):
                print('===========')
    
    # 变异
    for j in range(NP):
        r = np.random.random()
        if r <= Pm:
            for _ in range(1000):
                d = np.random.random(3)
                m = np.random.random()
                x1 = x[j]+m*d
                if st(x1):
                    x[j] = x1
                    break
                m = np.random.random()*m
                x1 = x[j]+m*d
                if st(x1):
                    x[j] = x1
                    break

print(v0,f0)
