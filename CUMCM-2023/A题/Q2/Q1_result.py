import math
import numpy as np
import pandas as pd
from sun_vector import sun_vector
from class_mirror import mirror
import itertools
from etas import *


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
    df = pd.read_csv(r'mirror_loc.csv')
    df.columns = ['x', 'y']
    df['(x,y)'] = list(zip(df['x'],df['y'],df.index+1))
    for date, hour in itertools.product(dates, hours):
        sun_vec = sun_vector(hour, phi=39.4, date='20220121')

        df['mirrors'] = df['(x,y)'].apply(lambda x: mirror(x[2],x[0],x[1]))
        df['normal_vec'] = df['mirrors'].apply(lambda x: mirror.normal_vector(x, sun_vec))
        df['eta_cos'] = df['mirrors'].apply(lambda x: mirror.eta_cos(x, sun_vec)*100)
        df['eta'] = eta()                   # todo get a series

        sin_alpha_s = sun_vector(hour, date=date, askfor='sin_alpha_s', phi=39.4)
        E_field = dni(sin_alpha_s)*sum(df['light_area']*df['eta'])

if __name__ == '__main__':
    main()