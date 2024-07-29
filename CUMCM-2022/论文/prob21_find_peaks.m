etaps=[1:10:100000];
p=zeros(1,10000);
for i = 1:10000
p(i)=powerp(etaps(i));
end
plot(etaps,p,'o-','MarkerSize',3)
hold on
[b,i]=sort(p);
plot(etaps(i(end-9:end)),b(end-9:end),'*','MarkerSize',15)
max=sum(b(end-9:end))/10;
index=sum(etaps(i(end-9:end)))/10;

function dxz=odefunqq(t,xz,etap)
V=(4866+2433)/1025; 
V1=1/3*pi*0.8; 
x0=-(V-V1)/pi;
z0=x0+0.5-2433*9.8/80000;
ro=1025;g=9.8;M=1165.992;w=2.2143;etax=167.8395;L0=0.5;mx=4866;mz=2433;r=1;f=4890;k=80000;
%%二维的变量，xz(1)=x，xz(2)=z,xz(3)=vx,xz(4)=vz 
dxz=zeros(4,1); 
dxz(1)=xz(3); 
dxz(2)=xz(4);
dxz(3)=(mz*g+ro*g*pi*r*r*(x0-xz(1))+f*cos(w*t)-etax*xz(3)-k*(L0-xz(2)+xz(1))-etap*(xz(3)-xz(4)))/(mx+M) ;
dxz(4)=(k*(L0-xz(2)+xz(1))+etap*(xz(3)-xz(4))-mz*g)/mz; 
end

function p=powerp(etapx)
V=(4866+2433)/1025;
V1=1/3*pi*0.8;
x0=-(V-V1)/pi;
z0=x0+0.5-2433*9.8/80000;
x1=0;z1=0;
etap=etapx;
[~,xz1]=ode45(@(t,xz1)odefunqq(t,xz1,etap),[0:0.2:40*2*pi/2.2143],[x0;z0;x1;z1]);
vxfu=xz1(:,3);
vzhen=xz1(:,4);
square=(vxfu(fix(20*2*pi/2.2143)*5:fix(40*2*pi/2.2143)*5)-vzhen(fix(20*2*pi/2.2143)*5:fix(40*2*pi/2.2143)*5)).^2; %%取第20至第40个周期稳定后的值来计算平均做功
area=1:(-fix(20*2*pi/2.2143)+fix(40*2*pi/2.2143))*5;
for i=1:-fix(20*2*pi/2.2143)*5+fix(40*2*pi/2.2143)*5
area(1,i)=(square(i,1)+square(i+1,1))*0.5*0.2;
end
p=etap*sum(area)/(20*2*pi/2.2143);
end




