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
        y.append(gauss(j,i,b1,c1)+gauss(j,a2,b2,c2))        
    for t in range(len(x)):
        arrayt.append([x[t],float(y[t])])
    
    df=pd.DataFrame(arrayt,columns=['波长（nm）','荧光数字信号强度'])
    df.to_excel('峰高比{:.3f}.xlsx'.format(i/a2),sheet_name='复合光谱')
    plt.plot(x,y)
plt.rcParams['font.sans-serif']=['SimHei']
plt.xlabel('波长(nm)')
plt.ylabel('荧光数字信号强度')
plt.savefig('峰高比1_to_9作图.png')
plt.show()
