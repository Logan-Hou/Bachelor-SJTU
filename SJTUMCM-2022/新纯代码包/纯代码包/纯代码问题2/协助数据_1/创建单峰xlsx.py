#单峰
from cmath import sqrt
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl

def gauss(x,a,b,c):             #只有峰强和波长是变量
    y=a*np.exp(-(x-b)**2/(2*c**2))
    return y
c1=22/(2*sqrt(np.log(4)))
c2=34/(2*sqrt(np.log(4)))
x=np.arange(100,700,0.6)
b1=400;b2=434
a1=np.arange(15000,140000,5000)
a2=15000
arrayt=[]

for i in a1:
    y=[]
    arrayt=[[]]
    for j in x:
        y.append(gauss(j,i,b1,c1))        
    for t in range(len(x)):
        arrayt.append([x[t],float(y[t])])
    
    df=pd.DataFrame(arrayt,columns=['波长（nm）','荧光数字信号强度'])
    df.to_excel('峰高比{:.3f}的单峰1.xlsx'.format(i/a2),sheet_name='单峰1')
    plt.plot(x,y)


for i in a1:
    y=[]
    arrayt=[[]]
    for j in x:
        y.append(gauss(j,a2,b2,c2))        
    for t in range(len(x)):
        arrayt.append([x[t],float(y[t])])
    
    df=pd.DataFrame(arrayt,columns=['波长（nm）','荧光数字信号强度'])
    df.to_excel('峰高比{:.3f}的单峰2.xlsx'.format(i/a2),sheet_name='单峰2')
    plt.plot(x,y)
