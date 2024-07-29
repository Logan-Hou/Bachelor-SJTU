import math
import numpy as np
import pandas as pd
from sun_vector import sun_vector
from class_mirror import mirror, normalize_vector
import itertools
# from etas import *
import warnings
import time
warnings.filterwarnings('ignore')


def eta_sb_optimized(mirror_i, sun_vec, mirror_list, width=6, height=6):
    start = time.time()

    ni = mirror_i.n
    list_x = np.linspace(-width/2, width/2, 10)
    list_y = np.linspace(-height/2, height/2, 10)
    l_i = normalize_vector(np.array([ni[1], -ni[0], 0]))
    r_i = normalize_vector(np.array([-ni[0] *ni[2], -ni[1] *ni[2], ni[0]**2 +ni[1]**2]))
    reflect_vec = mirror_i.reflect_vec

    count_series = pd.Series()
    for mirror_k in mirror_list:
        mirror_k.len2center = mirror.len2center(mirror_k, mirror_i)

    top5_list = sorted(mirror_list)[1:6]

    for xij, yij in itertools.product(list_x, list_y):
        count_series[f'({xij},{yij})'] = 0
        vec_xij = xij * l_i + yij * r_i + mirror_i.mirror_loc
        for mirror_k in top5_list:
            mirror_k_n = mirror_k.n
            l_k = normalize_vector(np.array([mirror_k_n[1], -mirror_k_n[0], 0]))
            r_k = normalize_vector(np.array([-mirror_k_n[0] * mirror_k_n[2], -mirror_k_n[1] * mirror_k_n[2], mirror_k_n[0] ** 2 + mirror_k_n[1] ** 2]))
            mirror_k_loc = mirror_k.mirror_loc
            dot_product_aijk = np.sum(mirror_k_n * (mirror_k_loc - vec_xij)) / np.sum(mirror_k_n * sun_vec)
            dot_product_bijk = np.sum(mirror_k_n * (mirror_k_loc - vec_xij)) / np.sum(mirror_k_n * reflect_vec)

            condition_a = np.abs(np.sum((vec_xij + dot_product_aijk * sun_vec - mirror_k_loc) * l_k)) >= width /2
            condition_b = np.abs(np.sum((vec_xij + dot_product_bijk * reflect_vec - mirror_k_loc) * r_k)) >= height /2

            if condition_a and condition_b:
                count_series[f'({xij},{yij})'] = 1

    eta_sb = 100 * count_series.sum() / len(count_series)
    end = time.time()
    print(end - start, 's')
    return eta_sb


def dni(sin_alpha_s):
    g0 = 1366
    H = 3
    a = 0.4237 - 0.000821*((6-H)**2)
    b = 0.5055 + 0.00595*((6.5-H)**2)
    c = 0.2711 + 0.01858*((2.5-H)**2)
    dni = g0 * (a+b*math.exp(-c/sin_alpha_s))
    return dni


def main():     # todo
    hours = [9, 10.5, 12, 13.5, 15]
    dates = [f"2022{str(i).rjust(2,'0')}21" for i in range(1,13)]
    df = pd.read_csv(r'C:\Users\Administrator\Desktop\2023国赛\A题\Q1\mirror_loc.csv')
    df.columns = ['x', 'y']
    df['(x,y)'] = list(zip(df['x'],df['y'],df.index+1))
    df['id'] = df.index+1
    for date, hour in itertools.product(dates, hours):
        sun_vec = sun_vector(hour, phi=39.4, date='20220121')

        df['mirrors'] = df['(x,y)'].apply(lambda x: mirror(x[2],x[0],x[1]))
        df['normal_vec'] = df['mirrors'].apply(lambda x: mirror.normal_vector(x, sun_vec))
        df['eta_cos'] = df['mirrors'].apply(lambda x: mirror.eta_cos(x, sun_vec)*100)
        mirror_list = list(df['mirrors'])
        df['eta_sb'] = df.apply(lambda x: eta_sb_optimized(x['mirrors'],sun_vec,mirror_list,width=6,height=6),axis=1)            # todo get a series

        sin_alpha_s = sun_vector(hour, date=date, askfor='sin_alpha_s', phi=39.4)
        E_field = dni(sin_alpha_s)*sum(df['light_area']*df['eta'])

if __name__ == '__main__':
    main()