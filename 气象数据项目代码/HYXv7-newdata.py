# 加载库
from netCDF4 import Dataset
import numpy as np
import sys
import tensorflow as tf
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import networkx as nx


def aaa(a,b):
    kk=0
    for item in b:
        if a[0]==item[0] and a[1]==item[1] and a[2]==item[2]:
            kk=1
            return kk
    return kk

log_string="HanYongXiang:"

#windows操作系统下/改为\\,mac下为/
file_path = "{path}/{filename}".format(
    path=sys.path[0],
    filename='ghte2.nc'
)

print(log_string, '开始解析文件', file_path)
nc = Dataset(file_path)

for var in nc.variables.keys():
    print("nc.variables.keys()=",nc.variables.keys())
    print("var=",var)
    path = sys.path[0]+'/'+var   #windows操作系统下/改为\\,mac下为/
    data = nc.variables[var][:]
    print(path)
    print(data.shape)
    print("len(data)=", len(data))
    print("len(data[0]=",len(data[0]))
    print("len(data[0][0]=", len(data[0][0]))
    #print("len(data[0][0][0]=", len(data[0][0][0]))
    #print(data)

    print(var , data.shape)
    print(log_string, path + '.npy', '数据写入')

print(data[0][0][0])
#print(len(data[0][0][0]))

f= open("data.txt", "w")   #设置文件对象

npdata=np.array(data)
npZerodata=np.where(npdata >= 4., npdata, 0.)
np.set_printoptions(threshold=100000)
for itemtemp in npZerodata:
    print(itemtemp)

np.set_printoptions(threshold=100000)
f.writelines(str(npZerodata))
print(str(npZerodata))
#print(len(npZerodata[0][0][0]))
print(len(npZerodata[0][0]))
#例如k为第0层第1行第45列，共134个值，有3个>4的值，可以作为测试
k=npZerodata[0][0][45]
print(k)
k=npZerodata[0][0][46]
print(k)

#构造循环，判定上下是否连通，以第0时刻的共44层为例，每层134*131
#这是11个时次的资料。垂直45层，X方向格点数134，Y方向格点数131.

#重要
#第一部分--------全部连通图计算
maxX=134
maxY=131
Layers=43
TIMEL=0  #11个时刻，从0-10
x=0
y=0
x0=0
y0=0
layer1=0
#将所有2点通路存放入一个数组path2Point
path2Point = np.empty(shape=[0, 6])
#path2Point = np.append(path2Point, [[1,2,3,4,5,6]], axis = 0)
#path2Point = np.append(path2Point, [[1,2,3,4,7,8]], axis = 0)
G=nx.DiGraph()


#格式为：层数，y坐标，x坐标

f.writelines("第一部分")
f.writelines("格式为(0,45,27)-(1,45,27)*(0,45,32)-(1,45,32)，其中-代表连通，*代表下一条线段开始：\n")
f.writelines("时刻坐标："+str(TIMEL)+"\n")

while layer1<Layers:
    while y<=maxY:
        while x<=maxX:
            if(npZerodata[layer1][y][x]>=4):
                #测试上层9个点
                if (npZerodata[layer1+1][y][x] >= 4):  #正上方
                    myData = "("+str(layer1)+","+str(y)+","+str(x)+")-"+"("+str(layer1+1)+","+str(y)+","+str(x)+")*"
                    f.writelines(str(myData))
                    path2Point = np.append(path2Point, [[layer1,y,x,layer1+1,y,x]], axis=0)
                    #将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                    #n = "123"   s = n.zfill(5)
                    #下方的'1'为时刻数，1-11
                    edgP1=int('1'+str(layer1).zfill(3)+str(y).zfill(3)+str(x).zfill(3))
                    edgP2=int('1'+str(layer1+1).zfill(3)+str(y).zfill(3)+str(x).zfill(3))
                    print(edgP1,edgP2)
                    G.add_edge(edgP1,edgP2)
                if (npZerodata[layer1+1][(y-1 < 0 and  y or y-1)][(x-1 < 0 and  x or x-1)] >= 4):  #左下方
                    myData = "(" + str(layer1) +","+ str(y) + "," + str(x) + ")-" + "(" + str(layer1 + 1)+"," + str(
                        y - 1 < 0 and y or y - 1) + "," + str(x-1 < 0 and  x or x-1) + ")*"
                    f.writelines(str(myData))
                    path2Point = np.append(path2Point, [[layer1, y, x, layer1 + 1, (y-1 < 0 and  y or y-1), (x-1 < 0 and  x or x-1)]], axis=0)
                    # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                    # n = "123"   s = n.zfill(5)
                    # 下方的'1'为时刻数，1-11
                    edgP1 = int('1' + str(layer1).zfill(3) + str(y).zfill(3) + str(x).zfill(3))
                    edgP2 = int('1' + str(layer1 + 1).zfill(3) + str((y-1 < 0 and  y or y-1)).zfill(3) + str(x-1 < 0 and  x or x-1).zfill(3))
                    print(edgP1, edgP2)
                    G.add_edge(edgP1, edgP2)
                if (npZerodata[layer1+1][(y-1 < 0 and  y or y-1)][x] >= 4):  #下方
                    myData = "(" + str(layer1) +","+ str(y) + "," + str(x) + ")-" + "(" + str(layer1 + 1)+"," + str(
                        y-1 < 0 and  y or y-1) + "," + str(x) + ")*"
                    f.writelines(str(myData))
                    path2Point = np.append(path2Point, [[layer1, y, x, layer1 + 1, (y-1 < 0 and  y or y-1), x]], axis=0)
                    # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                    # n = "123"   s = n.zfill(5)
                    # 下方的'1'为时刻数，1-11
                    edgP1 = int('1' + str(layer1).zfill(3) + str(y).zfill(3) + str(x).zfill(3))
                    edgP2 = int('1' + str(layer1 + 1).zfill(3) + str((y-1 < 0 and  y or y-1)).zfill(3) + str(x).zfill(3))
                    print(edgP1, edgP2)
                    G.add_edge(edgP1, edgP2)

                if (npZerodata[layer1 + 1][(y - 1 < 0 and y or y - 1)][(x+1 > maxX and  x or x+1)] >= 4):  # 右下方
                    myData = "(" + str(layer1) +","+ str(y) + "," + str(x) + ")-" + "(" + str(layer1 + 1)+"," + str(
                        y - 1 < 0 and y or y - 1) + "," + str(x+1 > maxX and  x or x+1) + ")*"
                    f.writelines(str(myData))
                    path2Point = np.append(path2Point, [[layer1, y, x, layer1 + 1, (y - 1 < 0 and y or y - 1), (x+1 > maxX and  x or x+1)]], axis=0)
                    # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                    # n = "123"   s = n.zfill(5)
                    # 下方的'1'为时刻数，1-11
                    edgP1 = int('1' + str(layer1).zfill(3) + str(y).zfill(3) + str(x).zfill(3))
                    edgP2 = int(
                        '1' + str(layer1 + 1).zfill(3) + str(y - 1 < 0 and y or y - 1).zfill(3) + str(x+1 > maxX and  x or x+1).zfill(3))
                    print(edgP1, edgP2)
                    G.add_edge(edgP1, edgP2)
                if (npZerodata[layer1 + 1][y][(x -1 < 0 and x or x -1)] >= 4):  # 左方
                    myData = "(" + str(layer1) +","+ str(y) + "," + str(x) + ")-" + "(" + str(layer1 + 1) +","+ str(
                        y) + "," + str(x -1 < 0 and x or x -1) + ")*"
                    f.writelines(str(myData))
                    path2Point = np.append(path2Point, [[layer1, y, x, layer1 + 1, y, (x -1 < 0 and x or x -1)]], axis=0)
                    # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                    # n = "123"   s = n.zfill(5)
                    # 下方的'1'为时刻数，1-11
                    edgP1 = int('1' + str(layer1).zfill(3) + str(y).zfill(3) + str(x).zfill(3))
                    edgP2 = int(
                        '1' + str(layer1 + 1).zfill(3) + str(y).zfill(3) + str(
                            x -1 < 0 and x or x -1).zfill(3))
                    print(edgP1, edgP2)
                    G.add_edge(edgP1, edgP2)
                if (npZerodata[layer1 + 1][y][(x+1 > maxX and  x or x+1)] >= 4):  # 右方
                    myData = "(" + str(layer1) +","+ str(y) + "," + str(x) + ")-" + "(" + str(layer1 + 1)+"," + str(
                        y) + "," + str(x+1 > maxX and  x or x+1) + ")*"
                    f.writelines(str(myData))
                    path2Point = np.append(path2Point, [[layer1, y, x, layer1 + 1, y, (x+1 > maxX and  x or x+1)]], axis=0)
                    # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                    # n = "123"   s = n.zfill(5)
                    # 下方的'1'为时刻数，1-11
                    edgP1 = int('1' + str(layer1).zfill(3) + str(y).zfill(3) + str(x).zfill(3))
                    edgP2 = int(
                        '1' + str(layer1 + 1).zfill(3) + str(y).zfill(3) + str(
                            x+1 > maxX and  x or x+1).zfill(3))
                    print(edgP1, edgP2)
                    G.add_edge(edgP1, edgP2)

                if (npZerodata[layer1 + 1][(y+1 > maxY and  y or y+1)][(x -1 < 0 and x or x -1)] >= 4):  # 左上方
                    myData = "(" + str(layer1) +","+ str(y) + "," + str(x) + ")-" + "(" + str(layer1 + 1) +","+ str(
                        y+1 > maxY and  y or y+1) + "," + str(x -1 < 0 and x or x -1) + ")*"
                    f.writelines(str(myData))
                    path2Point = np.append(path2Point, [[layer1, y, x, layer1 + 1, (y+1 > maxY and  y or y+1), (x -1 < 0 and x or x -1)]], axis=0)
                    # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                    # n = "123"   s = n.zfill(5)
                    # 下方的'1'为时刻数，1-11
                    edgP1 = int('1' + str(layer1).zfill(3) + str(y).zfill(3) + str(x).zfill(3))
                    edgP2 = int(
                        '1' + str(layer1 + 1).zfill(3) + str(y+1 > maxY and  y or y+1).zfill(3) + str(
                            x -1 < 0 and x or x -1).zfill(3))
                    print(edgP1, edgP2)
                    G.add_edge(edgP1, edgP2)

                if (npZerodata[layer1 + 1][(y+1 > maxY and  y or y+1)][x] >= 4):  # 上方
                    myData = "(" + str(layer1)+"," + str(y) + "," + str(x) + ")-" + "(" + str(layer1 + 1)+"," + str(
                        y+1 > maxY and  y or y+1) + "," + str(x) + ")*"
                    f.writelines(str(myData))
                    path2Point = np.append(path2Point, [[layer1, y, x, layer1 + 1, (y+1 > maxY and  y or y+1), x]], axis=0)
                    # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                    # n = "123"   s = n.zfill(5)
                    # 下方的'1'为时刻数，1-11
                    edgP1 = int('1' + str(layer1).zfill(3) + str(y).zfill(3) + str(x).zfill(3))
                    edgP2 = int(
                        '1' + str(layer1 + 1).zfill(3) + str(y+1 > maxY and  y or y+1).zfill(3) + str(
                            x).zfill(3))
                    print(edgP1, edgP2)
                    G.add_edge(edgP1, edgP2)

                if (npZerodata[layer1 + 1][(y+1 > maxY and  y or y+1)][x+1 > maxX and  x or x+1] >= 4):  # 右上方
                    myData = "(" + str(layer1) +","+ str(y) + "," + str(x) + ")-" + "(" + str(layer1 + 1)+"," + str(
                        y+1 > maxY and  y or y+1) + "," + str(x+1 > maxX and  x or x+1) + ")*"
                    f.writelines(str(myData))
                    path2Point = np.append(path2Point, [[layer1, y, x, layer1 + 1, (y+1 > maxY and  y or y+1), (x+1 > maxX and  x or x+1)]], axis=0)
                    # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                    # n = "123"   s = n.zfill(5)
                    # 下方的'1'为时刻数，1-11
                    edgP1 = int('1' + str(layer1).zfill(3) + str(y).zfill(3) + str(x).zfill(3))
                    edgP2 = int(
                        '1' + str(layer1 + 1).zfill(3) + str(y+1 > maxY and  y or y+1).zfill(3) + str(
                            x+1 > maxX and  x or x+1).zfill(3))
                    print(edgP1, edgP2)
                    G.add_edge(edgP1, edgP2)

            x=x+1
        y=y+1
        x=0
    layer1=layer1+1
    y=0


np.set_printoptions(threshold=100000)
print(path2Point)
f.writelines('\n---------------------------------------------------\n')
f.writelines('第二部分：以下为正式点位图，每行6元素，代表两个点（层数、y、x），代表此直线连通')
f.writelines("时刻坐标："+str(TIMEL)+"\n")
f.writelines(str(path2Point))

#所有2点通路存放在数组path2Point中，再建一个类似数组path2PointFrom0，只保留从第0层开始，向上第所有直线，若直线起点在0层以上则忽略
path2PointFrom0=np.empty(shape=[0, 6])
i=0
k=0
#第一步，将第0层数据全部写入path2PointFrom0
for temp1 in path2Point:
    if (temp1[0] == 0.):
        path2PointFrom0 = np.append(path2PointFrom0,[temp1],axis=0)

#目前path2PointFrom0已经具有了所有第0层和第一层第联通数据，现在从第2层开始，只要后三个数据相同则保存入新矩阵
#翟亮添加
'''
k=1
def pptest():
    for temp1 in path2PointFrom0:
        for temp2 in path2Point:
            if temp2[0]==temp1[3]:
                if temp1[3] == temp2[0] and temp1[4] == temp2[1] and temp1[5] == temp2[2]:
                    path2PointFrom0 = np.append(path2PointFrom0, [temp2], axis=0)
                    print('path2PointFrom0 temp1=',temp1)
                    print('path2Point temp2=',temp2)

'''
# 两两节点之间最短加权路径和长度。写入文件。采用NetxorkX标准all_pairs_dijkstra_path函数和、nx.all_pairs_dijkstra_path_length函数生成
f.writelines('\n---------------------------------------------------\n')
f.writelines('第三部分：两两节点之间最短加权路径和长度，采用NetxorkX标准all_pairs_dijkstra_path函数和、nx.all_pairs_dijkstra_path_length函数生成')
f.writelines("时刻坐标："+str(TIMEL)+"\n")
path1 = dict(nx.all_pairs_dijkstra_path(G))
length1 = dict(nx.all_pairs_dijkstra_path_length(G))
print('\n两两节点之间最短加权路径和长度: ', path1, length1)
f.writelines(str(path1)+str(length1))


#画图
#先利用
#nx.draw(G, with_labels=True)
#nx.draw(G)
#plt.title('有向图')
#plt.axis('on')
#plt.xticks([])
#plt.yticks([])
#plt.show()
'''
# 打开画图窗口2，在三维空间中绘图,本此绘制所有直线
fig = plt.figure(1)
ax = fig.gca(projection='3d')

# 给出2点直线坐标[ 42.  85.  67.  43.  84.  67.]，格式为z = [42, 43] y = [85, 84] x = [67, 67]
for temp in path2Point:
    fx=[temp[2],temp[5]]
    fy=[temp[1],temp[4]]
    fz = [temp[0], temp[3]]

    # 将数组中的前两个点进行连线
    figure = ax.plot(fx, fy, fz, c='r')
ax.set_xlabel('x label', color='r')
ax.set_ylabel('y label', color='g')
ax.set_zlabel('z label', color='b')#给三个坐标轴注明



plt.show()
#print(path2Point[0])
#print(path2PointFrom0)
'''


#构造循环，判定上下是否连通，以第0时刻的共44层为例，每层134*131
#这是11个时次的资料。垂直45层，X方向格点数134，Y方向格点数131.

#重要
#第二部分--------底层（第0层）连通图计算
N0maxX=134
N0maxY=131
N0Layers=43
N0TIMEL=TIMEL  #11个时刻，从0-10
N0x=0
N0y=0
N0x0=0
N0y0=0
N0layer1=0
#将所有2点通路存放入一个数组path2Point
N0path2Point = np.empty(shape=[0, 6])
#path2Point = np.append(path2Point, [[1,2,3,4,5,6]], axis = 0)
#path2Point = np.append(path2Point, [[1,2,3,4,7,8]], axis = 0)
N0G=nx.DiGraph()
#构造一个新数组，存放入选点位3维数组
N0path2PThisPoint = np.empty(shape=[0, 3])

N0f= open("dataN0.txt", "w")   #设置文件对象
#格式为：层数，y坐标，x坐标

N0f.writelines("\n第0层第一部分")
N0f.writelines("\n格式为(0,45,27)-(1,45,27)*(0,45,32)-(1,45,32)，其中-代表连通，*代表下一条线段开始：\n")
N0f.writelines("时刻坐标："+str(TIMEL)+"\n")

while N0layer1<N0Layers:
    while N0y<=N0maxY:
        while N0x<=N0maxX:
            if(npZerodata[N0layer1][N0y][N0x]>=4):
                #测试上层9个点,由于只计算第0层数据，所以测试条件为：第0层正常执行，第一层之后（本层点若未在N0path2Point中出现过，则pass）
                mmm=np.asarray([float(N0layer1), float(N0y), float(N0x)])
                kkk=aaa(mmm , N0path2PThisPoint)
                if N0layer1 == 0 or kkk:
                    if (npZerodata[N0layer1+1][N0y][N0x] >= 4):  #正上方
                        N0myData = "("+str(N0layer1)+","+str(N0y)+","+str(N0x)+")-"+"("+str(N0layer1+1)+","+str(N0y)+","+str(N0x)+")*"
                        N0f.writelines(str(N0myData))
                        N0path2Point = np.append(N0path2Point, [[N0layer1,N0y,N0x,N0layer1+1,N0y,N0x]], axis=0)
                        N0path2PThisPoint = np.append(N0path2PThisPoint,[[N0layer1,N0y,N0x]], axis=0)     #新添加
                        N0path2PThisPoint = np.append(N0path2PThisPoint,[[N0layer1+1,N0y,N0x]], axis=0)   #新添加
                        #将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                        #n = "123"   s = n.zfill(5)
                        #下方的'1'为时刻数，1-11
                        N0edgP1=int('1'+str(N0layer1).zfill(3)+str(N0y).zfill(3)+str(N0x).zfill(3))
                        N0edgP2=int('1'+str(N0layer1+1).zfill(3)+str(N0y).zfill(3)+str(N0x).zfill(3))
                        print(N0edgP1,N0edgP2)
                        N0G.add_edge(N0edgP1,N0edgP2)

                    if (npZerodata[N0layer1+1][(N0y-1 < 0 and  N0y or N0y-1)][(N0x-1 < 0 and  N0x or N0x-1)] >= 4):  #左下方
                        N0myData = "(" + str(N0layer1) +","+ str(N0y) + "," + str(N0x) + ")-" + "(" + str(N0layer1 + 1)+"," + str(
                            N0y - 1 < 0 and N0y or N0y - 1) + "," + str(N0x-1 < 0 and  N0x or N0x-1) + ")*"
                        N0f.writelines(str(N0myData))
                        N0path2Point = np.append(N0path2Point, [[N0layer1, N0y, N0x, N0layer1 + 1, (N0y-1 < 0 and  N0y or N0y-1), (N0x-1 < 0 and  N0x or N0x-1)]], axis=0)
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1, N0y, N0x]], axis=0)  # 新添加
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1 + 1, (N0y-1 < 0 and  N0y or N0y-1), (N0x-1 < 0 and  N0x or N0x-1)]], axis=0)  # 新添加
                        # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                        # n = "123"   s = n.zfill(5)
                        # 下方的'1'为时刻数，1-11
                        N0edgP1 = int('1' + str(N0layer1).zfill(3) + str(N0y).zfill(3) + str(N0x).zfill(3))
                        N0edgP2 = int('1' + str(N0layer1 + 1).zfill(3) + str((N0y-1 < 0 and  N0y or N0y-1)).zfill(3) + str(N0x-1 < 0 and  x or N0x-1).zfill(3))
                        print(N0edgP1, N0edgP2)
                        N0G.add_edge(N0edgP1, N0edgP2)
                    if (npZerodata[N0layer1+1][(N0y-1 < 0 and  N0y or N0y-1)][N0x] >= 4):  #下方
                        N0myData = "(" + str(N0layer1) +","+ str(N0y) + "," + str(N0x) + ")-" + "(" + str(N0layer1 + 1)+"," + str(
                            N0y-1 < 0 and  N0y or N0y-1) + "," + str(N0x) + ")*"
                        N0f.writelines(str(N0myData))
                        N0path2Point = np.append(N0path2Point, [[N0layer1, N0y, N0x, N0layer1 + 1, (N0y-1 < 0 and  N0y or N0y-1), N0x]], axis=0)
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1, N0y, N0x]], axis=0)  # 新添加
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1 + 1, (
                            N0y-1 < 0 and  N0y or N0y-1), N0x]], axis=0)  # 新添加
                        # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                        # n = "123"   s = n.zfill(5)
                        # 下方的'1'为时刻数，1-11
                        N0edgP1 = int('1' + str(N0layer1).zfill(3) + str(N0y).zfill(3) + str(N0x).zfill(3))
                        N0edgP2 = int('1' + str(N0layer1 + 1).zfill(3) + str((N0y-1 < 0 and  N0y or N0y-1)).zfill(3) + str(N0x).zfill(3))
                        print(N0edgP1, N0edgP2)
                        N0G.add_edge(N0edgP1, N0edgP2)

                    if (npZerodata[N0layer1 + 1][(N0y - 1 < 0 and N0y or N0y - 1)][(N0x+1 > N0maxX and  N0x or N0x+1)] >= 4):  # 右下方
                        N0myData = "(" + str(N0layer1) +","+ str(N0y) + "," + str(N0x) + ")-" + "(" + str(N0layer1 + 1)+"," + str(
                            N0y - 1 < 0 and N0y or N0y - 1) + "," + str(x+1 > N0maxX and  N0x or N0x+1) + ")*"
                        N0f.writelines(str(N0myData))
                        N0path2Point = np.append(N0path2Point, [[N0layer1, N0y, N0x, N0layer1 + 1, (N0y - 1 < 0 and N0y or N0y - 1), (N0x+1 > N0maxX and  N0x or N0x+1)]], axis=0)
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1, N0y, N0x]], axis=0)  # 新添加
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1 + 1, (N0y - 1 < 0 and N0y or N0y - 1), (N0x+1 > N0maxX and  N0x or N0x+1)]], axis=0)  # 新添加
                        # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                        # n = "123"   s = n.zfill(5)
                        # 下方的'1'为时刻数，1-11
                        N0edgP1 = int('1' + str(N0layer1).zfill(3) + str(N0y).zfill(3) + str(N0x).zfill(3))
                        N0edgP2 = int(
                            '1' + str(N0layer1 + 1).zfill(3) + str(N0y - 1 < 0 and N0y or N0y - 1).zfill(3) + str(N0x+1 > N0maxX and  N0x or N0x+1).zfill(3))
                        print(N0edgP1, N0edgP2)
                        N0G.add_edge(N0edgP1, N0edgP2)
                    if (npZerodata[N0layer1 + 1][N0y][(N0x -1 < 0 and N0x or N0x -1)] >= 4):  # 左方
                        N0myData = "(" + str(N0layer1) +","+ str(N0y) + "," + str(N0x) + ")-" + "(" + str(N0layer1 + 1) +","+ str(
                            N0y) + "," + str(N0x -1 < 0 and N0x or N0x -1) + ")*"
                        N0f.writelines(str(N0myData))
                        N0path2Point = np.append(N0path2Point, [[N0layer1, N0y, N0x, N0layer1 + 1, N0y, (N0x -1 < 0 and N0x or N0x -1)]], axis=0)
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1, N0y, N0x]], axis=0)  # 新添加
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1 + 1, N0y, (N0x -1 < 0 and N0x or N0x -1)]], axis=0)  # 新添加
                        # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                        # n = "123"   s = n.zfill(5)
                        # 下方的'1'为时刻数，1-11
                        N0edgP1 = int('1' + str(N0layer1).zfill(3) + str(N0y).zfill(3) + str(N0x).zfill(3))
                        N0edgP2 = int(
                            '1' + str(N0layer1 + 1).zfill(3) + str(N0y).zfill(3) + str(
                                N0x -1 < 0 and N0x or N0x -1).zfill(3))
                        print(N0edgP1, N0edgP2)
                        N0G.add_edge(N0edgP1, N0edgP2)
                    if (npZerodata[N0layer1 + 1][N0y][(N0x+1 > N0maxX and  N0x or N0x+1)] >= 4):  # 右方
                        N0myData = "(" + str(N0layer1) +","+ str(N0y) + "," + str(N0x) + ")-" + "(" + str(N0layer1 + 1)+"," + str(
                            N0y) + "," + str(N0x+1 > N0maxX and  N0x or N0x+1) + ")*"
                        N0f.writelines(str(N0myData))
                        N0path2Point = np.append(N0path2Point, [[N0layer1, N0y, N0x, N0layer1 + 1, N0y, (N0x+1 > N0maxX and  N0x or N0x+1)]], axis=0)
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1, N0y, N0x]], axis=0)  # 新添加
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1 + 1, N0y, (N0x+1 > N0maxX and  N0x or N0x+1)]], axis=0)  # 新添加
                        # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                        # n = "123"   s = n.zfill(5)
                        # 下方的'1'为时刻数，1-11
                        N0edgP1 = int('1' + str(N0layer1).zfill(3) + str(N0y).zfill(3) + str(N0x).zfill(3))
                        N0edgP2 = int(
                            '1' + str(N0layer1 + 1).zfill(3) + str(N0y).zfill(3) + str(
                                N0x+1 > N0maxX and  N0x or N0x+1).zfill(3))
                        print(N0edgP1, N0edgP2)
                        N0G.add_edge(N0edgP1, N0edgP2)

                    if (npZerodata[N0layer1 + 1][(N0y+1 > N0maxY and  N0y or N0y+1)][(N0x -1 < 0 and N0x or N0x -1)] >= 4):  # 左上方
                        N0myData = "(" + str(N0layer1) +","+ str(N0y) + "," + str(N0x) + ")-" + "(" + str(N0layer1 + 1) +","+ str(
                            N0y+1 > N0maxY and  N0y or N0y+1) + "," + str(N0x -1 < 0 and N0x or N0x -1) + ")*"
                        N0f.writelines(str(N0myData))
                        N0path2Point = np.append(N0path2Point, [[N0layer1, N0y, N0x, N0layer1 + 1, (N0y+1 > N0maxY and  N0y or N0y+1), (N0x -1 < 0 and N0x or N0x -1)]], axis=0)
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1, N0y, N0x]], axis=0)  # 新添加
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1 + 1, (N0y+1 > N0maxY and  N0y or N0y+1), (N0x -1 < 0 and N0x or N0x -1)]], axis=0)  # 新添加
                        # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                        # n = "123"   s = n.zfill(5)
                        # 下方的'1'为时刻数，1-11
                        N0edgP1 = int('1' + str(N0layer1).zfill(3) + str(N0y).zfill(3) + str(N0x).zfill(3))
                        N0edgP2 = int(
                            '1' + str(N0layer1 + 1).zfill(3) + str(N0y+1 > N0maxY and  N0y or N0y+1).zfill(3) + str(
                                N0x -1 < 0 and N0x or N0x -1).zfill(3))
                        print(N0edgP1, N0edgP2)
                        G.add_edge(N0edgP1, N0edgP2)

                    if (npZerodata[N0layer1 + 1][(N0y+1 > N0maxY and  N0y or N0y+1)][N0x] >= 4):  # 上方
                        N0myData = "(" + str(N0layer1)+"," + str(N0y) + "," + str(N0x) + ")-" + "(" + str(N0layer1 + 1)+"," + str(
                            N0y+1 > N0maxY and  N0y or N0y+1) + "," + str(N0x) + ")*"
                        N0f.writelines(str(N0myData))
                        N0path2Point = np.append(N0path2Point, [[N0layer1, N0y, N0x, N0layer1 + 1, (N0y+1 > N0maxY and  N0y or N0y+1), N0x]], axis=0)
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1, N0y, N0x]], axis=0)  # 新添加
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1 + 1, (N0y+1 > N0maxY and  N0y or N0y+1), N0x]], axis=0)  # 新添加
                        # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                        # n = "123"   s = n.zfill(5)
                        # 下方的'1'为时刻数，1-11
                        N0edgP1 = int('1' + str(N0layer1).zfill(3) + str(N0y).zfill(3) + str(N0x).zfill(3))
                        N0edgP2 = int(
                            '1' + str(N0layer1 + 1).zfill(3) + str(N0y+1 > N0maxY and  N0y or N0y+1).zfill(3) + str(
                                N0x).zfill(3))
                        print(N0edgP1, N0edgP2)
                        N0G.add_edge(N0edgP1, N0edgP2)

                    if (npZerodata[N0layer1 + 1][(N0y+1 > N0maxY and  N0y or N0y+1)][N0x+1 > N0maxX and  N0x or N0x+1] >= 4):  # 右上方
                        N0myData = "(" + str(N0layer1) +","+ str(N0y) + "," + str(N0x) + ")-" + "(" + str(N0layer1 + 1)+"," + str(
                            N0y+1 > N0maxY and  N0y or N0y+1) + "," + str(N0x+1 > N0maxX and  N0x or N0x+1) + ")*"
                        N0f.writelines(str(N0myData))
                        N0path2Point = np.append(N0path2Point, [[N0layer1, N0y, N0x, N0layer1 + 1, (N0y+1 > N0maxY and  N0y or N0y+1), (N0x+1 > N0maxX and  N0x or N0x+1)]], axis=0)
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1, N0y, N0x]], axis=0)  # 新添加
                        N0path2PThisPoint = np.append(N0path2PThisPoint, [[N0layer1 + 1, (N0y+1 > N0maxY and  N0y or N0y+1), N0x+1 > N0maxX and  N0x or N0x+1]], axis=0)  # 新添加
                        # 将这两个点，加入有向图G中，节点名称为该坐标直接str（)
                        # n = "123"   s = n.zfill(5)
                        # 下方的'1'为时刻数，1-11
                        N0edgP1 = int('1' + str(N0layer1).zfill(3) + str(N0y).zfill(3) + str(N0x).zfill(3))
                        N0edgP2 = int(
                            '1' + str(N0layer1 + 1).zfill(3) + str(N0y+1 > N0maxY and  N0y or N0y+1).zfill(3) + str(
                                N0x+1 > N0maxX and  N0x or N0x+1).zfill(3))
                        print(N0edgP1, N0edgP2)
                        N0G.add_edge(N0edgP1, N0edgP2)

            N0x=N0x+1
        N0y=N0y+1
        N0x=0
    N0layer1=N0layer1+1
    N0y=0
    N0x=0


np.set_printoptions(threshold=100000)
print(N0path2Point)
N0f.writelines('\n---------------------------------------------------')
N0f.writelines('\n第0层第二部分：以下为正式点位图，每行6元素，代表两个点（层数、y、x），代表此直线连通')
N0f.writelines("\n时刻坐标："+str(N0TIMEL)+"\n")
N0f.writelines(str(N0path2Point))


# 两两节点之间最短加权路径和长度。写入文件。采用NetxorkX标准all_pairs_dijkstra_path函数和、nx.all_pairs_dijkstra_path_length函数生成
N0f.writelines('\n---------------------------------------------------')
N0f.writelines('\n第0层第三部分：两两节点之间最短加权路径和长度，采用NetxorkX标准all_pairs_dijkstra_path函数和、nx.all_pairs_dijkstra_path_length函数生成')
N0f.writelines("\n时刻坐标："+str(N0TIMEL)+"\n")
N0path1 = dict(nx.all_pairs_dijkstra_path(N0G))
N0length1 = dict(nx.all_pairs_dijkstra_path_length(N0G))
print('\n两两节点之间最短加权路径和长度: ', N0path1, N0length1)
N0f.writelines(str(N0path1)+str(N0length1))


#画图
#先利用
#nx.draw(N0G, with_labels=True)
#nx.draw(N0G)
#plt.title('有向图')
#plt.axis('on')
#plt.xticks([])
#plt.yticks([])
#plt.show()

# 打开画图窗口3，在三维空间中绘图,本此绘制所有从第0层开始的直线
fig2 = plt.figure(1)
ax2 = fig2.gca(projection='3d')

# 给出2点直线坐标[ 42.  85.  67.  43.  84.  67.]，格式为z = [42, 43] y = [85, 84] x = [67, 67]
for temp in N0path2Point:
    fx=[temp[2],temp[5]]
    fy=[temp[1],temp[4]]
    fz = [temp[0], temp[3]]

    # 将数组中的前两个点进行连线
    figure2 = ax2.plot(fx, fy, fz, c='r')
ax2.set_xlabel('x0 label', color='r')
ax2.set_ylabel('y0 label', color='g')
ax2.set_zlabel('z0 label', color='b')#给三个坐标轴注明



plt.show()

#print(path2Point[0])
#print(path2PointFrom0)

f.close()
N0f.close()
nc.close()
print('N0path2PThisPoint=',N0path2PThisPoint)