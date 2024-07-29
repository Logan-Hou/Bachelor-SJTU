import math
import numpy as np
import pandas as pd
from sun_vector import sun_vector

def eta_sb(): # todo huge workload!!!!!
    return

def eta_at(d_hr):
    eta_at = 0.99321 - 0.0001176*d_hr + d_hr**2*1.97e-8
    return

def eta_trunc(): # todo huge workload!!!!
    return

eta_ref = 0.92
def eta()->pd.Series:
    returns