

import pandas as pd

from utils.setup import *


@verbose
def table_cont(df, columns):
    t = {}

    for col in columns:
        df[col+"Continuous"] = df.groupby('defCaseID')[col].transform('nunique')
        for r in df['race'].unique():
            t[r] = {df[df['race']==r]}
            t[r][col] = df[col+"Continuous"].value_counts()
    return pd.concat(t, keys=columns)

@verbose
def table_cat(df, columns):
    t = {}
    for col in columns:
        t[col] = pd.crosstab(df['race'], df[col], margins=True, margins_name='Total').T
    for col, table in t.items():
        s = pd.concat(t, keys=columns)
    return s

@verbose
def global_out(filename):
    with open(filename, "w") as file:
        for name, value in globals().items():
            if name.isupper():
                file.write(f"{name}: {value}\n")

