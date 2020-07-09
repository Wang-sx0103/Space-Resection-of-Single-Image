import sys
import os
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
#from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog
#from PyQt5.QtGui import *

from GUI import Ui_MainWindow

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(mywindow, self).__init__()  #super(mywindow,self) 首先找到 mywindowd的父类(也就是类 QtWidgets.QMainWindow, Ui_MainWindow)
                                          #然后把类 mywindow 的对象转换为父类的对象 
        self.setupUi(self)
        #self.dataBrowser.setFont(QtGui.QFont("Microsoft YaHei"))
        self.setWindowTitle("单像空间后方交会")
        self.data = []
        self.pointNum = 0                                             #控制点数量
        self.dataButton.clicked.connect(self.onClickImportDataButton)
        self.calButton.clicked.connect(self.onClickCalButton)
    
    def initialize(self):
        self.x0 = self.y0 = self.f0 = self.w0 = self.k0 = 0
        self.f = 153.24
        self.x = [0 for i in range(self.pointNum)]                    #量测的像点坐标x
        self.y = [0 for i in range(self.pointNum)]                    #量测的像点坐标y
        self.X = [0 for i in range(self.pointNum)]                    #实际地面控制点X
        self.Y = [0 for i in range(self.pointNum)]                    #实际地面控制点Y
        self.Z = [0 for i in range(self.pointNum)]                    #实际地面控制点Z
        self.x0 = eval(self.xinit.toPlainText())                      #框标坐标系与像主点坐标系x差值
        self.y0 = eval(self.yinit.toPlainText())                      #框标坐标系与像主点坐标系y差值
        self.f = eval(self.fd.toPlainText())                          #投影中心到像平面中心的距离f
        self.f0 = eval(self.finit.toPlainText())                      #外方位角元素的初始值
        self.w0 = eval(self.winit.toPlainText())
        self.k0 = eval(self.kinit.toPlainText())
        #print(x0)
        for i in range(len(self.data)):
            #print(self.data[i].split(",")[3])
            self.x[i] = float(self.data[i].split(",")[0])
            self.y[i] = float(self.data[i].split(",")[1])
            self.X[i] = float(self.data[i].split(",")[2])
            self.Y[i] = float(self.data[i].split(",")[3])
            self.Z[i] = float(self.data[i].split(",")[4])
        self.X0s = sum(self.X)/self.pointNum                          #外方位线元素的初始值
        self.Y0s = sum(self.Y)/self.pointNum
        self.Z0s = sum(self.Z)/self.pointNum + 72.260

    def RMatrix(self,f,w,k):
        Rf = np.mat([[np.cos(f), 0, -np.sin(f)],
              [0,         1,          0],
              [np.sin(f), 0,  np.cos(f)]])

        Rw = np.mat([[1,         0,          0],
              [0, np.cos(w), -np.sin(w)],
              [0, np.sin(w),  np.cos(w)]])
    
        Rk = np.mat([[np.cos(k), -np.sin(k), 0],
              [np.sin(k),  np.cos(k), 0],
              [0,         0,          1]])
    
        R = Rf*Rw*Rk
        return R

    def xyApproximate(self,X,Y,Z,x,y,Xs,Ys,Zs,R):
        xApxm = [0 for i in range(self.pointNum)]
        yApxm = [0 for i in range(self.pointNum)]
        for i in range(self.pointNum):
            xApxm[i] = x[i] - (self.x0 - self.f*((R[0,0]*(X[i]-Xs)+R[1,0]*(Y[i]-Ys)+R[2,0]*(Z[i]-Zs))
                                /(R[0,2]*(X[i]-Xs)+R[1,2]*(Y[i]-Ys)+R[2,2]*(Z[i]-Zs))))    #即x0(0位于右上角)- x
            yApxm[i] = y[i] - (self.y0 - self.f*((R[0,1]*(X[i]-Xs)+R[1,1]*(Y[i]-Ys)+R[2,1]*(Z[i]-Zs))
                                /(R[0,2]*(X[i]-Xs)+R[1,2]*(Y[i]-Ys)+R[2,2]*(Z[i]-Zs))))

        return xApxm,yApxm

    def AParameter(self,X,Y,Z,Xs,Ys,Zs,x,y,w,k,R):
        parameter = np.zeros((2,6))                       #一个点的常数矩阵
        mean = np.zeros((3,1))
        minus = np.zeros((3,1))
        minus = np.array([[X-Xs],
                     [Y-Ys],
                     [Z-Zs]])
        mean = R.T * np.mat(minus)
        parameter[0][0] = (R[0,0]*self.f+R[0,2]*(x-self.x0))/mean[2]
        parameter[0][1] = (R[1,0]*self.f+R[1,2]*(x-self.x0))/mean[2]
        parameter[0][2] = (R[2,0]*self.f+R[2,2]*(x-self.x0))/mean[2]
        parameter[1][0] = (R[0,1]*self.f+R[0,2]*(y-self.y0))/mean[2]
        parameter[1][1] = (R[1,1]*self.f+R[1,2]*(y-self.y0))/mean[2]
        parameter[1][2] = (R[2,1]*self.f+R[2,2]*(y-self.y0))/mean[2]

        parameter[0][3] = (y-self.y0)*np.sin(w)-(((x-self.x0)/self.f)*((x-self.x0)*np.cos(k)-(y-self.y0)*np.sin(k))+self.f*np.cos(k))*np.cos(w)
        parameter[0][4] = -self.f*np.sin(k)-((x-self.x0)/self.f)*((x-self.x0)*np.sin(k)+(y-self.y0)*np.cos(k))
        parameter[0][5] = y-self.y0
        parameter[1][3] = -(x-self.x0)*np.sin(w)-(((y-self.y0)/self.f)*((x-self.x0)*np.cos(k)-(y-self.y0)*np.sin(k))-self.f*np.cos(k))*np.cos(w)
        parameter[1][4] = -self.f*np.cos(k)-((y-self.y0)/self.f)*((x-self.x0)*np.sin(k)+(y-self.y0)*np.cos(k))
        parameter[1][5] = -(x-self.x0)
    
        return parameter

    def onClickImportDataButton(self):
        printStr = ""
        filePath , _ = QFileDialog.getOpenFileName(self,'数据获取','\\',"text files (*.csv )")

        if os.path.exists(filePath):
            with open(filePath,"r",encoding = "utf-8") as file:
                self.data = file.readlines()
            self.pointNum = len(self.data)
            
            for i in range(len(self.data)):
                printStr = printStr+self.data[i]
            
            self.dataBrowser.setText(printStr)

        else:
            if printStr != "" :
                self.dataBrowser.setPlainText(printStr)

    def onClickCalButton(self):
        #正餐
        self.initialize()
        xApxm = [0 for i in range(self.pointNum)]
        yApxm = [0 for i in range(self.pointNum)]
        R = np.mat(np.zeros((3,3)))
        l = np.mat(np.zeros((self.pointNum*2,1)))
        A = np.mat(np.zeros((self.pointNum*2,6)))
        fdelta=wdelta=kdelta = 1
        flag = 0
        while(abs(fdelta)>0.000001) | (abs(wdelta)>0.000001) | (abs(kdelta)>0.000001):
            R = self.RMatrix(self.f0,self.w0,self.k0)                          #使用近似值f0、w0、k0，构建旋转矩阵
            xApxm,yApxm = self.xyApproximate(self.X,self.Y,self.Z,self.x,self.y,self.X0s,self.Y0s,self.Z0s,R) #计算通过近似值求算出的像点坐标于量测坐标的差
            #构建常数矩阵l
            for i in range(self.pointNum):
                l[2*i] = xApxm[i]
                l[2*i+1] = yApxm[i]
            #构建系数矩阵A
            for j in range(self.pointNum):
                A[2*j:2*j+2,:] = self.AParameter(self.X[j],self.Y[j],self.Z[j],self.X0s,self.Y0s,self.Z0s,self.x[j],self.y[j],self.w0,self.k0,R)
            xMatrix = np.mat(np.zeros((6,1)))
            xMatrix = (A.T*A).I*A.T*l                                          #通过最小二乘法求解出误差向量
            fdelta = xMatrix[3,0]
            wdelta = xMatrix[4,0]
            kdelta = xMatrix[5,0]
            self.X0s = self.X0s + xMatrix[0,0]                                 #求得的误差与带求值（给定初值）相加
            self.Y0s = self.Y0s + xMatrix[1,0]
            self.Z0s = self.Z0s + xMatrix[2,0]
            self.f0 = self.f0 + fdelta
            self.w0 = self.w0 + wdelta
            self.k0 = self.k0 + kdelta
            if flag<100:
                flag = flag+1
            else:
                self.iterations.setText("级数不收敛!")
                break
        if flag<100:
            self.iterations.setText(str(flag))
        """printstr = "Xs:  "+str(round(self.X0s,3)) + "m\n" + "Ys:  "+str(round(self.Y0s,3))+"m\n" +\
                   "Zs:  "+str(round(self.Z0s,3))+"m\n" + "f:   "+str(round(self.f0,3))+"\n" + \
                   "w:   "+str(round(self.w0,3))+"\n" + "k:   "+str(round(self.k0,3))+"\n" """
        
        self.iterations.setText(str(flag))
        self.textBrowser.setText(str(round(self.X0s,3)))
        self.textBrowser_2.setText(str(round(self.Y0s,3)))
        self.textBrowser_3.setText(str(round(self.Z0s,3)))
        self.textBrowser_4.setText(str(round(self.f0,3)))
        self.textBrowser_5.setText(str(round(self.w0,3)))
        self.textBrowser_6.setText(str(round(self.k0,3)))

if __name__ == '__main__': 
    
    app = QApplication(sys.argv)
    mainwindow = mywindow()
    mainwindow.show()
    sys.exit(app.exec_())