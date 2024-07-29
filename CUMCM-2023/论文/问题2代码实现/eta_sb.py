import itertools
import math
import time

import numpy as np
import pandas as pd
from sun_vector import sun_vector
from class_mirror import mirror
from eta_trunc import eta_trunc_1point


def normalize_vector(vector):
    return vector/np.linalg.norm(vector)

def eta_sb(mirror_i,sun_vec,r_shadow,l_shadow,tan_alpha_s,width=6,height=6,center_z=4):
    alpha_list = np.linspace(0, 4.65e-3, 4)
    beta_list = np.linspace(0, 7/4 * np.pi, 8)
    mirror_i_loc = mirror_i.mirror_loc
    top5_list = mirror_i.top5_list       # exclude itself

    # 大柱子挡住 直接返回
    xij_r_shadow = np.dot(mirror_i_loc,r_shadow)
    if xij_r_shadow > 0 and xij_r_shadow <= 84 / tan_alpha_s and abs(np.dot(mirror_i_loc, l_shadow)) <= 3.5 and mirror_i_loc[2] / (
            84 / tan_alpha_s - xij_r_shadow) <= tan_alpha_s:
        return [0,0]

    ni = mirror_i.n; ni_x = ni[0];ni_y = ni[1];ni_z = ni[2]
    list_x = np.linspace(-width/2, width/2, 4)
    list_y = np.linspace(-height/2, height/2, 4)
    l_i = normalize_vector(np.array([ni_y, -ni_x, 0]))
    r_i = normalize_vector(np.array([-ni_x*ni_z, -ni_y*ni_z, ni_x**2+ni_y**2]))
    reflect_vec = mirror_i.reflect_vec
    count_df = pd.DataFrame({'eta_sb':[]})


    for xij, yij in itertools.product(list_x,list_y):
        count_df.loc[f'({xij},{yij})','eta_sb'] = 0
        vec_xij = xij*l_i + yij*r_i + mirror_i_loc
        for mirror_k in top5_list:
            mirror_k_n = mirror_k.n
            mirror_k_loc = mirror_k.mirror_loc
            nk_x = mirror_k_n[0]
            nk_y = mirror_k_n[1]
            nk_z = mirror_k_n[2]
            l_k = normalize_vector(np.array([nk_y, -nk_x, 0]))
            r_k = normalize_vector(np.array([-nk_x * nk_z, -nk_y * nk_z, nk_x ** 2 + nk_y ** 2]))
            aijk = vec_xij + np.dot(mirror_k_n,(mirror_k_loc-vec_xij))/np.dot(mirror_k_n, sun_vec)*sun_vec
            bijk = vec_xij + np.dot(mirror_k_n,(mirror_k_loc-vec_xij))/np.dot(mirror_k_n, reflect_vec)*reflect_vec

            if abs(np.dot((aijk - mirror_k_loc),l_k)) >= width/2:
                if abs(np.dot((aijk - mirror_k_loc),r_k)) >= height/2:
                    if abs(np.dot((bijk - mirror_k_loc),l_k)) >= width/2:
                        if abs(np.dot((bijk - mirror_k_loc) ,r_k)) >= height/2:
                            count_df.loc[f'({xij},{yij})','eta_sb'] = 1
                            count_df.loc[f'({xij},{yij})','eta_trunc_1point'] = eta_trunc_1point(reflect_vec,vec_xij,alpha_list,beta_list)


    eta_sb = sum(count_df['eta_sb'])/len(count_df['eta_sb'])
    count_trunc = count_df[count_df['eta_sb'] == 1].copy()
    eta_trunc_whole = count_trunc['eta_trunc_1point'].mean()

    return [eta_sb,eta_trunc_whole]


def eta_at(d_hr):
    eta_at = 0.99321 - 0.0001176*d_hr + d_hr**2*1.97e-8
    return eta_at

