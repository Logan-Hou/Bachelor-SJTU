from fileinput import filename
from turtle import distance
from unicodedata import name
from scipy.signal import argrelextrema
from numpy import *
from pandas import *
from matplotlib.pyplot import *
from scipy import signal
import heapq
for filenames in ['蓝绿黄','绿黄红']:
    a=read_excel(filenames+'.xlsx')
    print(filenames)
    b=a['波长（nm）']

    c=a['荧光数字信号强度']
    d=-c
    #方法
    num_peak_3=signal.find_peaks(c,distance=50)
    num_peak_4=signal.find_peaks(d,distance=20)
    peak=[]
    leastpeak=[]
    excelarray=[]
    dictionary={}
    plot(b,c,'r',label='original values')
    #极大值
    for ii in range(len(num_peak_3[0])):
        if c[num_peak_3[0][ii]]>20000:          #剔除坏点
            plot(b[num_peak_3[0][ii]],c[num_peak_3[0][ii]],'*',markersize=10) 
            print('峰值的波长',b[num_peak_3[0][ii]],'nm');print('峰值的荧光数字信号强度',c[num_peak_3[0][ii]])
            peak.append(num_peak_3[0][ii])          #波峰的索引
            excelarray.append(['第{}个波峰的强度'.format(peak.index(num_peak_3[0][ii])+1),c[num_peak_3[0][ii]]])
            excelarray.append(['第{}个波峰的中心波长'.format(peak.index(num_peak_3[0][ii])+1),b[num_peak_3[0][ii]]])
    #极小值
    for ii in range(len(num_peak_4[0])):
        if  d[num_peak_4[0][ii]]<-5000 :          #剔除坏点
            dictionary[d[num_peak_4[0][ii]]]=num_peak_4[0][ii]          #用-极小值做键，索引做值
            leastpeak.append(d[num_peak_4[0][ii]])
    least_min=heapq.nlargest(2,leastpeak)
    for i in range(len(least_min)):
        plot(b[dictionary[least_min[i]]],-least_min[i],'*',markersize=10) 
        print('峰谷的波长',b[dictionary[least_min[i]]],'nm');print('峰谷的荧光数字信号强度',-least_min[i])
        excelarray.append(['第{}个波谷的强度'.format(i+1),-least_min[i]])
    c_base=c[1:100].mean()
    for i in range(len(peak)):  
        height=c[peak[i]]-c_base

        xs=[x for x in range(len(c)) if (c[x]-c_base)>(height/2) ]
        min_b_distance=min(abs(min(b[x] for x in xs)-b[peak[i]]),abs(b[peak[i]]-b[dictionary[least_min[0]]]),abs(b[peak[i]]-b[dictionary[least_min[1]]]))
        max_b_distance=min(abs(max(b[x] for x in xs)-b[peak[i]]),abs(b[peak[i]]-b[dictionary[least_min[0]]]),abs(b[peak[i]]-b[dictionary[least_min[1]]]))   
        if min_b_distance <= max_b_distance:                #取到正确的半波宽的对应横坐标（波长）x
            xs=[x for x in xs if abs(b[x]-b[peak[i]]) <= min_b_distance]
            bxs=[b[x] for x in xs]
            cxs=[c[x] for x in xs]
            plot(bxs,cxs,'b-')
            t=min(min_b_distance,abs(min(bxs)-b[peak[i]]))
            lambda_b=2*t
            print('第',i+1,'个峰的复合图像上的半波宽为：',lambda_b,'nm')
        else:
            xs=[x for x in xs if abs(b[x]-b[peak[i]]) <= max_b_distance]
            bxs=[b[x] for x in xs]
            cxs=[c[x] for x in xs]
            plot(bxs,cxs,'b-')
            t=min(max_b_distance,abs(min(bxs)-b[peak[i]]))
            lambda_b=2*t
            print('第',i+1,'个峰的复合图像上的半波宽为：',lambda_b,'nm')
        excelarray.append(['第{}个峰的半峰宽'.format(i+1),lambda_b])
    rcParams['font.sans-serif']=['SimHei']
    rcParams['axes.unicode_minus']=False

    xlabel('波长(nm)')
    ylabel('荧光数字信号强度')
    name=filenames + '的波峰特征值提取.png'
    savefig(name)

    df=DataFrame(excelarray,columns=['index','values'])
    df.to_excel(filenames+'的特征值数据.xlsx')
    show()