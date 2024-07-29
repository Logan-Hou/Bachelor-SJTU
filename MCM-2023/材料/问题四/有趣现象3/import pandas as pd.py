import pandas as pd
from pandas import read_csv
import numpy as np
import matplotlib.pyplot as plt

a_list=[0,0,0,0,0]
e_list=[0,0,0,0,0]
i_list=[0,0,0,0,0]
o_list=[0,0,0,0,0]
u_list=[0,0,0,0,0]

alloflist=[0,0,0,0,0]

file=pd.read_excel('Problem_C_Data_Wordle.xlsx')
list1=file.Word[:-1]
print(list1)
class often_words(object):
      def __init__(self,word,frequency):
            self.word=word
            self.frequency=frequency
      def __lt__(self,other):
            return self.frequency < other.frequency
for  i in list1:
    for j in range(len(i)):
        if i[j]=='a':
            a_list[j]+=1
            alloflist[j]+=1

        if i[j]=='e':
            e_list[j]+=1
            alloflist[j]+=1

        if i[j]=='i':
            i_list[j]+=1
            alloflist[j]+=1

        if i[j]=='o':
            o_list[j]+=1
            alloflist[j]+=1

        if i[j]=='u':
            u_list[j]+=1
            alloflist[j]+=1
all_list=[a_list,e_list,i_list,o_list,u_list]
print(all_list)
plt.figure()
plt.style.use('seaborn')

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

color_list='rgbym'
word_list='aeiou'
# 画图，plt.bar()可以画柱状图
plt.subplot(121)
for i in range(len(all_list)):
    plt.plot(range(1,6),all_list[i],color=color_list[i],marker='*',label=word_list[i])    
    
# 设置图片名称all_list[i]
plt.title("aeiou元音字母在5个位置的使用频数")
# 设置x轴标签名
plt.xlabel("位置顺序")
# 设置y轴标签名
plt.ylabel("使用频数")
plt.legend()
# 显示

plt.subplot(122)
plt.plot(range(1,6),alloflist,marker='*',label='频数')
plt.title("所有元音字母在5个位置上的频数")
plt.xlabel("位置顺序")
# 设置y轴标签名
plt.ylabel("使用频数")
plt.legend()
plt.show()
