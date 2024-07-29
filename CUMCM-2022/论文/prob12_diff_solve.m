clear
clc
format long
V=(4866+2433)/1025;
V1=1/3*pi*0.8;
x0=-(V-V1)/pi;
z0=x0+0.5-2433*9.8/80000;
x1=0;z1=0;
[t,xz]=ode45('odefun2',[0:0.02:40*2*pi/1.4005],[x0;z0;x1;z1]);   %作图
[t1,xz1]=ode45('odefun2',[0:0.2:40*2*pi/1.4005],[x0;z0;x1;z1]);     %excel
[t2,xz2]=ode45('odefun2',[0:10:120],[x0;z0;x1;z1]);  %论文
%plot(t,xz(:,1),'-',t,xz(:,2),'-')%浮子与振子位置
plot(t,xz(:,3),'-',t,xz(:,4),'-')%浮子与振子速度

xfu=xz1(:,1)-x0;
zzhen=xz1(:,2)-z0;
vxfu=xz1(:,3);
vzhen=xz1(:,4);
