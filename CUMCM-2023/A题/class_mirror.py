import numpy as np
import pandas as pd
from sun_vector import sun_vector



def normalize_vector(vector):
    return vector/np.linalg.norm(vector)


class mirror(object):
    tower_loc = np.array([0, 0, 80])

    def __init__(self, name, x, y, center_z=4, length=6, width=6):
        self.top5_list = None
        self.len2center = None
        self.eta_cos = None
        self.n = None
        self.light_area = None
        self.name = name
        self.x = x
        self.y = y
        self.center_z = center_z
        self.length = length
        self.width = width
        self.area = length * width
        # 镜子中心坐标
        self.mirror_loc = np.array([self.x, self.y, self.center_z])
        # 单位反射光线向量
        self.reflect_vec = normalize_vector(self.tower_loc - self.mirror_loc)
        # 计算大气透射率
        self.d_hr = np.linalg.norm(self.tower_loc - self.mirror_loc)

    # 镜面单位法向量
    def normal_vector(self, sun_vec):
        n = -sun_vec + self.reflect_vec
        n = n/np.linalg.norm(n)
        self.n = n
        return n

    def eta_cos(self, sun_vec):
        eta_cos = abs(sum(sun_vec * self.n))
        self.eta_cos = eta_cos
        return eta_cos

    def len2center(self,other):
        len2center = np.linalg.norm(self.mirror_loc - other.mirror_loc)
        return len2center
    
    def top5_close(self, mirror_list):
        for mirror_k in mirror_list:
            mirror_k.len2center = mirror.len2center(mirror_k, self)
        top5_list = sorted(mirror_list)[1:5]
        self.top5_list = top5_list
        return self

    def __lt__(self, other):
        return self.len2center < other.len2center
    # # 采光面积 用法向量和入射光线来算
    # def light_area(self, sun_vec, area=36):
    #     cos_theta = sum(sun_vec * self.n)
    #     self.light_area = area*cos_theta
    #     return area*cos_theta

def main():
    hour = 9
    sun_vec = sun_vector(hour, askfor='i')
    x, y = 150, -150
    mirror1 = mirror('mirror1', x, y)
    print('Successful Class')

if __name__ == '__main__':
    main()

