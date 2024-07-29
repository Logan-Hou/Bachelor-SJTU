p2 =  -0.2169;
p1 =  6.616e-06;
x0=-p2/p1;
knp_best=(x0+100000)/2;
alpha_best=knp_best*p1+p2;

p_best=powerp2(knp_best,alpha_best);

function dxz=odefunqq2(t,xz,knp,alpha)
V=(4866+2433)/1025; 
V1=1/3*pi*0.8; 
x0=-(V-V1)/pi;
z0=x0+0.5-2433*9.8/80000;
ro=1025;g=9.8;M=1165.992;w=2.2143;etax=167.8395;L0=0.5;mx=4866;mz=2433;r=1;f=4890;k=80000;
%%二维的变量，xz(1)=x，xz(2)=z,xz(3)=vx,xz(4)=vz 
dxz=zeros(4,1); 
dxz(1)=xz(3); 
dxz(2)=xz(4);
dxz(3)=(mz*g+ro*g*pi*r*r*(x0-xz(1))+f*cos(w*t)-etax*xz(3)-k*(L0-xz(2)+xz(1))-knp*abs(xz(3)-xz(4)).^alpha*(xz(3)-xz(4)))/(mx+M) ;
dxz(4)=(k*(L0-xz(2)+xz(1))+knp*abs(xz(3)-xz(4)).^alpha*(xz(3)-xz(4)))/mz; 
end

function p=powerp2(knpx,alpha)
V=(4866+2433)/1025;
V1=1/3*pi*0.8;
x0=-(V-V1)/pi;
z0=x0+0.5-2433*9.8/80000;
x1=0;z1=0;
knp=knpx;
[~,xz1]=ode45(@(t,xz1)odefunqq2(t,xz1,knp,alpha),[0:0.2:40*2*pi/2.2143],[x0;z0;x1;z1]);
vxfu=xz1(:,3);
vzhen=xz1(:,4);
fix1=fix(20*2*pi/2.2143);fix2=fix(40*2*pi/2.2143);
square=abs(vxfu(fix1*5:fix2*5)-vzhen(fix1*5:fix2*5)).^(alpha+2); %%取20-40个周期稳定后的值来计算平均做功
area=1:(-fix1+fix2)*5;
for i=1:-fix1*5+fix2*5
area(1,i)=(square(i,1)+square(i+1,1))*0.1;
end
p=knp*sum(area)/(20*2*pi/2.2143);
end

