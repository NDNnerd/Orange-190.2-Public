import os

import pandas as pd

from utils.list_counter import list_counter
from utils.risk import calculate_risk
from utils.setup import *


@verbose
def calc_app_count(df, col, pool):
    count = list_counter(df, col, drop_low_freq=True, low_freq=20)
    df = df[df[col].isin(count[col].tolist().unique())]
    D = {}
    for d in D[col].unique():
        D[d] = calculate_risk(df, df[df[col]==d], df[df[pool] == 1], 'race')
    return D