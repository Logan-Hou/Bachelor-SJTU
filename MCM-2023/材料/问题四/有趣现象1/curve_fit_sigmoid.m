a_mod =     0.03553  ;
b_mod =      0.3674  ;
c_mod=     0.01658 ;
       

[a,b]=xlsread('input4.xlsx');
a1=a(:,1);
a2=a(:,2);
a3=1:357;
rate_a=[];
y= a_mod./(b_mod+exp(-c_mod*a3));%拟合函数f(x)=a/(b+exp(-c*x))
for i = 1:357
    rate_a(i)=a2(i)/a1(i);
end
rate_a=rate_a(end:-1:1);
plot(a3,rate_a,'-*b','LineWidth',0.7,'Markersize',3)
hold on
plot(a3,y,'-r','LineWidth',2); %线性，颜色，标记
axis([0,360,0,0.14])  %确定x轴与y轴框图大小
set(gca,'YTick',[0:0.02:0.14]) %x轴范围1-6，间隔1
set(gca,'XTick',[0:50:357]) %y轴范围0-700，间隔100
legend('困难模式','拟合sigmoid函数图像');   %右上角标注
xlabel('Dates from 2022/1/7 to 2022/12/31')  %x轴坐标描述
title('随着日期增长，选择困难模式的人数占比变化')
ylabel('选择困难模式人数占全部人数比例') %y轴坐标描述


% General model:
%      f(x) = a/(b+exp(-c*x))
% Coefficients (with 95% confidence bounds):
%        a =     0.03553  (0.03355, 0.03752)
%        b =      0.3674  (0.3479, 0.3869)
%        c =     0.01658  (0.01583, 0.01733)
% 
% Goodness of fit:
%   SSE: 0.005503
%   R-square: 0.9682
%   Adjusted R-square: 0.968
%   RMSE: 0.003943