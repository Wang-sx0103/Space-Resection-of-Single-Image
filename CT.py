# -*- coding: utf-8 -*-
#框标坐标转换为像平面坐标
import numpy as np

xFrame = [-106.003,-106.001,106.001,106.003,-110.001,-0.004,109.997,0.002]      #像平面坐标系下的8个点的坐标x1
yFrame = [-106.003,106.003,106.001,-106.005,0.002,110.004,0.0,-109.998]
xPixel = [153.928,196.331,4904.433,4861.645,86.497,2550.953,4971.761,2506.927]  #像素坐标系下的8个点的坐标x2
yPixel = [230.193,4938.664,4896.771,187.841,2585.143,5006.359,2541.754,120.266]

xControl = [4446,4389,4473,2548,2476,2570,634,517,451]                          #控制点的像素坐标
yControl = [4093,2503,909,3878,2226,1062,4113,2438,829]
xF = []                                                                         #控制点的像平面坐标，代求量
yF = []
aTranslation = []                                                               #坐标变换中的平移量
bFlexible = []                                                                  #坐标变换中的伸缩量，不难看出x、y轴有相同的伸缩量和平移量
dx = 1
dy = 1
x0 =  114.0
y0 =  22.0

while abs(dx)>0.00001 and abs(dy)>0.00001:
    x = np.mat(np.zeros((2,1)))
    T0 = xFrame[0]-x0
    T1 = xFrame[1]-x0
    T2 = xFrame[2]-x0
    T3 = xFrame[3]-x0
    T4 = xFrame[4]-x0
    T5 = xFrame[5]-x0
    T6 = xFrame[6]-x0
    T7 = xFrame[7]-x0
    A = np.mat([[y0,T0],[y0,T1],[y0,T2],[y0,T3],[y0,T4],[y0,T5],[y0,T6],[y0,T7]])
    aMatrix = np.mat(A)
    
    T0 = xPixel[0]-x0*y0-y0*xFrame[0]
    T1 = xPixel[1]-x0*y0-y0*xFrame[1]
    T2 = xPixel[2]-x0*y0-y0*xFrame[2]
    T3 = xPixel[3]-x0*y0-y0*xFrame[3]
    T4 = xPixel[4]-x0*y0-y0*xFrame[4]
    T5 = xPixel[5]-x0*y0-y0*xFrame[5]
    T6 = xPixel[6]-x0*y0-y0*xFrame[6]
    T7 = xPixel[7]-x0*y0-y0*xFrame[7]
    B = np.mat([T0,T1,T2,T3,T4,T5,T6,T7])#,dtype=np.float)
    bMatrix = np.mat(B)
    x = (A.T*A).I*A.T*B.T
    dx = x.tolist()[0][0]
    dy = x.tolist()[1][0]
    x0 = x0+dx
    y0 = y0+dy

print(x0)
print(y0)

for j in range(len(xControl)):
    x = xControl[j]/y0 - x0
    y = yControl[j]/y0 - x0
    xF.append(round(x,3))
    yF.append(round(y,3))
print(xF)
print(yF)
