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
xx0 =  114.0
xy0 =  22.0

while abs(dx)>0.000001 and abs(dy)>0.000001:
    x = np.mat(np.zeros((2,1)))
    T0 = xFrame[0]-xx0
    T1 = xFrame[1]-xx0
    T2 = xFrame[2]-xx0
    T3 = xFrame[3]-xx0
    T4 = xFrame[4]-xx0
    T5 = xFrame[5]-xx0
    T6 = xFrame[6]-xx0
    T7 = xFrame[7]-xx0
    A = np.mat([[xy0,T0],[xy0,T1],[xy0,T2],[xy0,T3],[xy0,T4],[xy0,T5],[xy0,T6],[xy0,T7]])
    T0 = xPixel[0]-xx0*xy0-xy0*xFrame[0]
    T1 = xPixel[1]-xx0*xy0-xy0*xFrame[1]
    T2 = xPixel[2]-xx0*xy0-xy0*xFrame[2]
    T3 = xPixel[3]-xx0*xy0-xy0*xFrame[3]
    T4 = xPixel[4]-xx0*xy0-xy0*xFrame[4]
    T5 = xPixel[5]-xx0*xy0-xy0*xFrame[5]
    T6 = xPixel[6]-xx0*xy0-xy0*xFrame[6]
    T7 = xPixel[7]-xx0*xy0-xy0*xFrame[7]
    B = np.mat([T0,T1,T2,T3,T4,T5,T6,T7])
    x = (A.T*A).I*A.T*B.T
    dx = x[0,0]
    dy = x[1,0]
    xx0 = xx0+dx
    xy0 = xy0+dy

print("x轴的平移量:",xx0)
print("x轴的平移量:",xy0)

dx = 1
dy = 1
yx0 =  114.0
yy0 =  22.0

while abs(dx)>0.000001 and abs(dy)>0.000001:
    x = np.mat(np.zeros((2,1)))
    T0 = yFrame[0]-yx0
    T1 = yFrame[1]-yx0
    T2 = yFrame[2]-yx0
    T3 = yFrame[3]-yx0
    T4 = yFrame[4]-yx0
    T5 = yFrame[5]-yx0
    T6 = yFrame[6]-yx0
    T7 = yFrame[7]-yx0
    A = np.mat([[yy0,T0],[yy0,T1],[yy0,T2],[yy0,T3],[yy0,T4],[yy0,T5],[yy0,T6],[yy0,T7]])
    T0 = yPixel[0]-yx0*yy0-yy0*yFrame[0]
    T1 = yPixel[1]-yx0*yy0-yy0*yFrame[1]
    T2 = yPixel[2]-yx0*yy0-yy0*yFrame[2]
    T3 = yPixel[3]-yx0*yy0-yy0*yFrame[3]
    T4 = yPixel[4]-yx0*yy0-yy0*yFrame[4]
    T5 = yPixel[5]-yx0*yy0-yy0*yFrame[5]
    T6 = yPixel[6]-yx0*yy0-yy0*yFrame[6]
    T7 = yPixel[7]-yx0*yy0-yy0*yFrame[7]
    B = np.mat([T0,T1,T2,T3,T4,T5,T6,T7])
    x = (A.T*A).I*A.T*B.T
    dx = x[0,0]
    dy = x[1,0]
    yx0 = yx0 + dx
    yy0 = yy0 + dy

print("y轴的平移量:",yx0)
print("y轴的伸缩量:",yy0)

for j in range(len(xControl)):
    x = xControl[j]/xy0 - xx0
    y = yControl[j]/yy0 - yx0
    xF.append(round(x,3))
    yF.append(round(y,3))
print("框标平面坐标下的x：",xF)
print("框标平面坐标下的y：",yF)
