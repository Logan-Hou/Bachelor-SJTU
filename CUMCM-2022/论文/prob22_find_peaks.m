
knps=[0:500:100000];
alpha=[0:0.05:1];
plist=zeros(201,21);%plist_k=zeros(201,21);plist_a=zeros(201,21);
figure(1);
for j=1:21
    for i = 1:201
    p=powerp2(knps(i),alpha(j));
    plist(i,j)=p;
    %plist_k(i,j)=i;plist_a(i,j)=j;
    scatter3(knps(i),alpha(j),p)
hold on
    end
end
[B,IX] = sort(plist(:),'descend');
[I,J] = ind2sub(size(plist),IX) ;
scatter3(knps(I(1:80)),alpha(J(1:80)),B(1:80),'filled')
max_k=knps(I(1:80));max_a=alpha(J(1:80));
hold off 
figure(2);
figure2=scatter(knps(I(1:80)),alpha(J(1:80)),'filled');%最大80个点在alpha和阻尼系数平面上的投影

% [m,im]=max(plist);
% [m2,im2]=max(m);
% i=im(im2);
% j=im2;
% k_index=knps(i);a_index=alpha(j);

% plot(knp,p,'o-','MarkerSize',3)
% hold on
% [b,i]=sort(p);
% plot(knp(i(end-9:end)),b(end-9:end),'*','MarkerSize',15)
% max=sum(b(end-9:end))/10;
% index=sum(knp(i(end-9:end)))/10;





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
