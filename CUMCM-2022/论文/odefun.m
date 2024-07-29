function dxz=odefun(t,xz)
V=(4866+2433)/1025; 
V1=1/3*pi*0.8; 
x0=-(V-V1)/pi;
z0=x0+0.5-2433*9.8/80000;
ro=1025;g=9.8;M=1335.535;w=1.4005;etax=656.3616;etap=10000;L0=0.5;mx=4866;mz=2433;r=1;f=6250;k=80000;
%%二维的变量，xz(1)=x，xz(2)=z,xz(3)=vx,xz(4)=vz 
dxz=zeros(4,1); 
dxz(1)=xz(3); 
dxz(2)=xz(4);
dxz(3)=(mz*g+ro*g*pi*r*r*(x0-xz(1))+f*cos(w*t)-etax*xz(3)-k*(L0-xz(2)+xz(1))-etap*(xz(3)-xz(4)))/(mx+M) ;
dxz(4)=(k*(L0-xz(2)+xz(1))+etap*(xz(3)-xz(4))-mz*g)/mz; 
end