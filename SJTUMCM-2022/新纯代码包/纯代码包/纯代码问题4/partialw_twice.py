from turtle import distance
from scipy.signal import argrelextrema
from numpy import *
from pandas import *
from matplotlib.pyplot import *
from scipy import signal
import heapq

a=read_excel('partial_twice.xlsx')
b=a['波长']
c=a['二次处理后的峰强']
d=-c
#方法1
num_peak_3=signal.find_peaks(c,distance=5)
num_peak_4=signal.find_peaks(d,distance=5)
peak=[]
leastpeak=[]
dictionary={}
excelarray=[]
new_peaklist=[]
plot(b,c,'r',label='original values')
#极大值
for ii in range(len(num_peak_3[0])):
    if c[num_peak_3[0][ii]]>40:          #剔除坏点
        new_peaklist.append(num_peak_3[0][ii])
        plot(b[num_peak_3[0][ii]],c[num_peak_3[0][ii]],'*',markersize=10) 
        print('峰值{}的波长'.format(new_peaklist.index(num_peak_3[0][ii])+1),b[num_peak_3[0][ii]],'nm');print('峰值的荧光数字信号强度',c[num_peak_3[0][ii]])
        peak.append(num_peak_3[0][ii])          #波峰的索引
        excelarray.append(['第{}个波峰的强度'.format(peak.index(num_peak_3[0][ii])+1),c[num_peak_3[0][ii]]])
        excelarray.append(['第{}个波峰的中心波长'.format(peak.index(num_peak_3[0][ii])+1),b[num_peak_3[0][ii]]])
#极小值
for ii in range(len(num_peak_4[0])):
    if  d[num_peak_4[0][ii]]>-50 and b[num_peak_4[0][ii]]>min(b[peak]):          #剔除坏点
        dictionary[d[num_peak_4[0][ii]]]=num_peak_4[0][ii]          #用-极小值做键，索引做值
        leastpeak.append(d[num_peak_4[0][ii]])
least_min=heapq.nlargest(5,leastpeak)               #取到三个波谷
for i in range(len(least_min)):
    
        plot(b[dictionary[least_min[i]]],-least_min[i],'*',markersize=10) 
        print('第{}个峰谷的波长'.format(i+1),b[dictionary[least_min[i]]],'nm');print('峰谷的荧光数字信号强度',-least_min[i])
        excelarray.append(['第{}个波谷的强度'.format(i+1),-least_min[i]])
        excelarray.append(['第{}个波谷的中心波长'.format(i+1),b[dictionary[least_min[i]]]])
xlabel('波长')
ylabel('二次微分处理后的信号强度')
title('复合光谱信号强度函数的二阶微分')
rcParams['font.sans-serif']=['SimHei']
rcParams['axes.unicode_minus']=False
df=DataFrame(excelarray,columns=['index','values'])
df.to_excel('partial_twice'+'的极大值极小值数据.xlsx')
show()