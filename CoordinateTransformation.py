# -*- coding: utf-8 -*-
#框标坐标转换为像平面坐标


"""xFrame = [-106.003,-106.001,106.001,106.003,-110.001,-0.004,109.997,0.002]      #像平面坐标系下的8个点的坐标x1
yFrame = [-106.003,106.003,106.001,-106.005,0.002,110.004,0.0,-109.998]
xPixel = [153.928,196.331,4904.433,4861.645,86.497,2550.953,4971.761,2506.927]  #像素坐标系下的8个点的坐标x2
yPixel = [230.193,4938.664,4896.771,187.841,2585.143,5006.359,2541.754,120.266]"""

xFrame = [-110.001,-0.004,109.997,0.002]                                        #像平面坐标系下的8个点的坐标x1
yFrame = [0.002,110.004,0.0,-109.998]
xPixel = [86.497,2550.953,4971.761,2506.927]                                    #像素坐标系下的8个点的坐标x2
yPixel = [2585.143,5006.359,2541.754,120.266]

xControl = [4446,4389,4473,2548,2476,2570,634,517,451]                          #控制点的像素坐标
yControl = [4093,2503,909,3878,2226,1062,4113,2438,829]
xF = []                                                                         #控制点的像平面坐标，代求量
yF = []
aTranslation = []                                                               #坐标变换中的平移量
bFlexible = []                                                                  #坐标变换中的伸缩量，不难看出x、y轴有相同的伸缩量和平移量
for i in range(len(xFrame)):
    a = (xPixel[i]*yFrame[i]-xFrame[i]*yPixel[i])/(yPixel[i]-xPixel[i])
    b = xPixel[i]/(xFrame[i] + a)
    aTranslation.append(a)
    bFlexible.append(b)
aMean = sum(aTranslation)/len(aTranslation)
bMean = sum(bFlexible)/len(bFlexible)
for j in range(9):
    x = xControl[j]/bMean - aMean
    y = yControl[j]/bMean - aMean
    xF.append(round(x,3))
    yF.append(round(y,3))
print(xF)
print(yF)