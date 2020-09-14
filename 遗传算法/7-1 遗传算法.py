# -*- coding: utf-8 -*-

import math
import numpy as np

def minGA(f, a, b, NP, NG, Pc, Pm, eps):
    '''
    f       目标函数
    a       自变量下界
    b       自变量上界
    NP      种群个体数
    NG      最大进化代数
    Pc      杂交概率
    Pm      变异概率
    eps     自变量离散精度
    
    返回目标函数最小值
    '''
    L = int(np.ceil(math.log2((b-a)/eps+1)))
    x = np.zeros((NP,L),dtype=int)
    fx = np.zeros(NP)
#    nx = np.zeros((NP,L), dtype=int)

    #种群初始化
    for i in range(NP):
        x[i] = np.random.randint(0,2,L)
    print(x)
    nx = x.copy()
    fx = [f(dec(a, b, x[i], L)) for i in range(NP)]
    
    for k in range(NG):
        # 所有个体适应值之和
        sumfx = sum(fx)
        # 所有个体适应值的权重
        Px = fx / sumfx    
        # 用于轮盘赌策略的概率累加
        PPx = np.cumsum(Px)

        for i in range(NP):
            sita = np.random.random()
            # 根据轮盘赌策略确定的父亲
            for n in range(NP):
                if sita < PPx[n]:
                    SelFather = n
                    break
        
            # 随机选择母亲
            Selmother = int(np.floor(np.random.random()*NP))
            #print('mother',Selmother)
#            Selmother = int(np.floor(np.random.random()*(NP))+1)

            # 随机确定交叉点
            posCut = int(np.floor(np.random.random()*(L-2)))

            # 交叉
            r1 = np.random.random()
            if r1 <= Pc:
                nx[i,:posCut+1] = x[SelFather,:posCut+1]
                nx[i,posCut+1:] = x[Selmother,posCut+1:]
            
            # 变异
            r2 = np.random.random()
            if r2 <= Pm:
#                    posMut = round(np.random.random()*(L-1))
                posMut = int(np.random.random()*L)
                nx[i,posMut] = 1 - nx[i, posMut]
            
        x = nx.copy()
        fx = [f(dec(a, b, x[i], L)) for i in range(NP)]

    i = np.argmax(fx)
    return [dec(a, b, x[i], L), fx[i]]
                
# 把将个体基因（形如[1,0,1,0,...]的数组）转变为a，b间的十进制数
def bin_dec(a,b,x,L):
    s = [chr(ord('0')+i) for i in x]
    y = ''.join(s)
    return int(y,2)*(b-a)/(2**L-1)

def dec(a,b,x,L):
    base = 2**np.arange(L-1, -1, -1)
    y = np.dot(base,x)
    return a + y*(b-a)/(2**L-1)

def t_minGA():
    f = lambda x: x**3 - 60*x**2 + 900*x + 100
    [xv, fv] = minGA(f, 0, 30, 50, 100, 0.9, 0.04, 0.01)
    print([xv, fv])

t_minGA()
    
