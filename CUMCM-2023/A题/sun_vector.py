import datetime as datetime
import itertools
import pandas as pd
import numpy as np
import math


# 太阳时角计算
def get_omega(hour=9):
    omega = math.pi/12*(hour-12)
    return omega


def sun_vector(hour, phi=39.4, date='20220621', askfor='i') -> np.array:
    phi = phi*math.pi/180
    omega = get_omega(hour)     # 太阳时角

    cos_omega = math.cos(omega)
    sin_phi = math.sin(phi)
    cos_phi = math.cos(phi)
    date0 = datetime.date(2022,3,21)
    date = datetime.date(int(date[:4]),int(date[4:6]),int(date[6:]))
    D = (date-date0).days

    sin_delta = math.sin(2*math.pi*D/365)*math.sin(23.45*2*math.pi/360)  # 太阳赤纬角计算
    cos_delta = math.sqrt(1-sin_delta**2)

    sin_alpha_s = cos_delta*cos_phi*cos_omega + sin_delta * sin_phi
    cos_alpha_s = math.sqrt(1-sin_alpha_s**2)

    cos_gamma_s = round((sin_delta - sin_alpha_s*sin_phi)/(cos_alpha_s*cos_phi),5)
    if hour>12:
        sin_gamma_s = math.sqrt(1-cos_gamma_s**2)
    else:
        sin_gamma_s = -math.sqrt(1-cos_gamma_s**2)
    # 入射光线方向向量：
    if askfor=='i':
        i = np.array([cos_alpha_s*sin_gamma_s,cos_alpha_s*-cos_gamma_s,-sin_alpha_s])
        return i
    elif askfor=='sin_alpha_s':
        return sin_alpha_s
    elif askfor=='hlg':
        alpha_s = round(np.rad2deg(math.acos(cos_alpha_s)),2)
        if hour>12:
            gamma_s = round(360-np.rad2deg(math.acos(cos_gamma_s)),2)
        else:
            gamma_s = round(np.rad2deg(math.acos(cos_gamma_s)),2)
        return f'({alpha_s},{gamma_s})'
    elif askfor=='alpha_gamma_s':
        return sin_gamma_s,cos_gamma_s,sin_alpha_s/cos_alpha_s
    else:
        return None


def hlg_csv():
    hours = [9, 10.5, 12, 13.5, 15]
    dates = [f"2022{str(i).rjust(2, '0')}21" for i in range(1, 13)]
    df = pd.DataFrame(index=dates, columns=hours)
    for date, hour in itertools.product(dates, hours):
        df.loc[date, hour] = sun_vector(hour, phi=39.4, date=date, askfor='hlg')
    return df


if __name__ == '__main__':
    df = hlg_csv()
    df.to_csv('angle.csv')