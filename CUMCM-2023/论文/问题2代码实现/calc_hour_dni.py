import datetime as datetime
import itertools
import pandas as pd
import numpy as np
import math
from sun_vector import sun_vector


def dni(sin_alpha_s):
    g0 = 1366
    H = 3
    a = 0.4237 - 0.000821*((6-H)**2)
    b = 0.5055 + 0.00595*((6.5-H)**2)
    c = 0.2711 + 0.01858*((2.5-H)**2)
    dni = g0 * (a+b*math.exp(-c/sin_alpha_s))
    return dni

def main():
    dates = [f"2022{str(i).rjust(2,'0')}21" for i in range(1,13)]
    hours = [9, 10.5, 12, 13.5, 15]

    series = pd.Series()
    for date, hour in itertools.product(dates, hours):
        sin_alpha_s = sun_vector(hour, date=date, askfor='sin_alpha_s', phi=39.4)
        series[f"{date} {hour}"] = dni(sin_alpha_s)

    series.name = 'DNI'
    series.to_csv('DNI.csv')

if __name__ == '__main__':
    main()