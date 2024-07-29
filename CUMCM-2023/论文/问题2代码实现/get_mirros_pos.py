import pandas as pd

from class_mirror import mirror, normalize_vector
import itertools
from eta_sb import *
import warnings
import time

def get_mirrors_pos(r1,r2,r3,r4,c1,c2,c3,c4,
                       w1,w2,w3,w4,h1,h2,h3,h4,y_tower):
    # 定义参数
    tower_x = 0
    tower_y = y_tower
    tower_z = 0
    tower_radius = 100
    num_iterations = 6 #迭代次数
    mirrors_num = np.random.randint(5e6,6e6)
    df = pd.DataFrame({'x':np.random.random(mirrors_num),'y':np.random.random(mirrors_num)})

    # 定义六个半径和对应的尺寸
    radii = [r1]*4
    sizes = [c1, w1, h1]*4

    # 循环验证
    for iteration in range(1, num_iterations+1):
        test_df = perform_iteration(iteration,df,'20220321',hour=12)
    df = test_df

    # 生成均匀分布的点
    for radius, size in zip(radii, sizes):
        # 计算每个圆环上均匀分布的点数量，这里假设为100个
        num_points = 100

        # 生成均匀分布的角度
        angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

        # 计算每个点的坐标
        x_coordinates = tower_x + radius * np.cos(angles)
        z_coordinates = tower_z + radius * np.sin(angles)

        # 创建一个DataFrame存储当前半径内的点
        radius_df = pd.DataFrame({'x': x_coordinates, 'y': tower_y, 'z': z_coordinates})

        # 添加尺寸信息
        radius_df['c'] = size[0]
        radius_df['w'] = size[1]
        radius_df['h'] = size[2]

        # 将当前半径内的点添加到总的DataFrame中
        df = df.append(radius_df, ignore_index=True)

    # 筛选出不在塔周围100米半径内的点
    distance_to_tower = np.sqrt((df['x'] - tower_x) ** 2 + (df['z'] - tower_z) ** 2)
    df = df[distance_to_tower > tower_radius]
    return df

def perform_iteration(iteration_number,df,date,hour):
    # 初始化参数
    df.columns = ['x', 'y']
    df['(x,y)'] = list(zip(df['x'],df['y'],df.index+1))
    df['id'] = df.index+1
    date_mean_table = pd.DataFrame({'hour': [], 'eta': [], 'eta_cos': [], 'eta_sb': [], 'eta_trunc': [], 'Efield': [], 'Efield_mirror_mean': []})
    hour_mean_table = {'hour': [], 'eta': [], 'eta_cos': [], 'eta_sb': [], 'eta_trunc': [], 'Efield': [],
                       'Efield_mirror_mean': []}

    df['mirrors'] = df['(x,y)'].apply(lambda x: mirror(x[2], x[0], x[1]))
    mirror_list = list(df['mirrors'])
    df['mirrors'] = df['mirrors'].apply(lambda x: mirror.top5_close(x, mirror_list))
    print('date',date)
    sun_vec = sun_vector(hour, phi=39.4, date=date)
    sin_alpha_s = sun_vector(hour, date=date, askfor='sin_alpha_s', phi=39.4)
    sin_gamma_s,cos_gamma_s,tan_alpha_s = sun_vector(hour, phi=39.4, date=date, askfor='alpha_gamma_s')
    r_shadow = np.array([-sin_gamma_s, -cos_gamma_s, 0])
    l_shadow = np.array([cos_gamma_s,-sin_gamma_s,0])
    df['eta_sb_trunc'] = df.apply(lambda x: eta_sb(x['mirrors'], sun_vec, r_shadow, l_shadow, tan_alpha_s, width=6, height=6), axis=1)
    return df

