import math
import numpy as np
import pandas as pd
from sun_vector import sun_vector
from class_mirror import mirror, normalize_vector
import itertools
from eta_sb import *
import warnings
import time
warnings.filterwarnings('ignore')
from eta_sb import eta_sb


def dni(sin_alpha_s):
    g0 = 1366
    H = 3
    a = 0.4237 - 0.000821*((6-H)**2)
    b = 0.5055 + 0.00595*((6.5-H)**2)
    c = 0.2711 + 0.01858*((2.5-H)**2)
    dni = g0 * (a+b*math.exp(-c/sin_alpha_s))
    return dni


def main():
    hours = [9, 10.5, 12, 13.5, 15]
    dates = [f"2022{str(i).rjust(2,'0')}21" for i in range(3,5)]
    df = pd.read_csv(r'C:\Users\Administrator\Desktop\2023国赛\A题\Q1\mirror_loc.csv')
    df.columns = ['x', 'y']
    df['(x,y)'] = list(zip(df['x'],df['y'],df.index+1))
    df['id'] = df.index+1
    date_mean_table = pd.DataFrame({'hour': [], 'eta': [], 'eta_cos': [], 'eta_sb': [], 'eta_trunc': [], 'Efield': [], 'Efield_mirror_mean': []})
    hour_mean_table = {'hour': [], 'eta': [], 'eta_cos': [], 'eta_sb': [], 'eta_trunc': [], 'Efield': [],
                       'Efield_mirror_mean': []}

    df['mirrors'] = df['(x,y)'].apply(lambda x: mirror(x[2], x[0], x[1]))
    mirror_list = list(df['mirrors'])
    df['mirrors'] = df['mirrors'].apply(lambda x: mirror.top5_close(x, mirror_list))

    for date, hour in itertools.product(dates, hours):
        start = time.time()
        print('date',date)
        sun_vec = sun_vector(hour, phi=39.4, date=date)
        sin_alpha_s = sun_vector(hour, date=date, askfor='sin_alpha_s', phi=39.4)
        sin_gamma_s,cos_gamma_s,tan_alpha_s = sun_vector(hour, phi=39.4, date=date, askfor='alpha_gamma_s')
        r_shadow = np.array([-sin_gamma_s, -cos_gamma_s, 0])
        l_shadow = np.array([cos_gamma_s,-sin_gamma_s,0])

        df['normal_vec'] = df['mirrors'].apply(lambda x: mirror.normal_vector(x, sun_vec))
        df['eta_cos'] = df['mirrors'].apply(lambda x: mirror.eta_cos(x, sun_vec))
        df['eta_at'] = df['mirrors'].apply(lambda x: eta_at(x.d_hr))
        df['mirror_i_loc'] = df['mirrors'].apply(lambda x: x.mirror_loc)
        df['mirror_area'] = df['mirrors'].apply(lambda x: x.area)

        # todo big work!!!!!!!!!!!!!!
        df['eta_sb_trunc'] = df.apply(lambda x: eta_sb(x['mirrors'],sun_vec,r_shadow,l_shadow,tan_alpha_s,width=6,height=6),axis=1)            # todo get a series

        df['eta_sb'] = df['eta_sb_trunc'].apply(lambda x: x[0])
        df['eta_trunc'] = df['eta_sb_trunc'].apply(lambda x: x[1])
        df['eta'] = df['eta_sb']*df['eta_at']*df['eta_cos']*df['eta_trunc']*0.92
        E_field = dni(sin_alpha_s)*sum(df['mirror_area']*df['eta'])
        hour_mean_table['hour'].append(hour)
        hour_mean_table['eta'].append(df['eta'].mean())
        hour_mean_table['eta_cos'].append(df['eta_cos'].mean())
        hour_mean_table['eta_sb'].append(df['eta_sb'].mean())
        hour_mean_table['eta_trunc'].append(df['eta_trunc'].mean())
        hour_mean_table['Efield'].append(E_field)
        hour_mean_table['Efield_mirror_mean'].append(E_field/sum(df['mirror_area']))
        end = time.time()
        print('一天一个时辰',end-start,'s')
        insert_df = pd.DataFrame(hour_mean_table)
        insert_df.to_csv(f'{date}{hour}.csv')
        if len(hour_mean_table['hour']) == 5:
            hour_mean_map = pd.DataFrame(hour_mean_table)
            hour_mean_map.to_csv(f'{date}.csv')
            date_mean_table.loc[date] = hour_mean_map.mean()
            hour_mean_table = {'hour': [], 'eta': [], 'eta_cos': [], 'eta_sb': [], 'eta_trunc': [], 'Efield': [],
                       'Efield_mirror_mean': []}

    date_mean_table.to_csv('Q1.csv')
if __name__ == '__main__':
    main()