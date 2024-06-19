import pandas as pd

from utils.setup import *

Y = "\033[1;38;5;157m" 
u = "\033[4m" 
y = "\033[0;38;5;157m" 
B = "\033[1;4;38;5;33m" 
b = "\033[0;38;5;33m" 
G = "\033[1;4;38;5;46m" 
g = "\033[0;38;5;46m" 
Rr = "\033[1;4;38;5;196m" 
rr = "\033[0;38;5;196m" 
S = "\033[0m" 

@verbose
def tab(df, col):
    c =  df[col].value_counts()
    n = df[col].value_counts(normalize=True)
    t = {}
    for k, v in c.items():
        n[k] = round(n[k]*100, 2)
        t[k] = (v, n[k])
        print(f"{y}{k}: {v} {Y}({n[k]}%){S}")
    print(f"{b}Total: {B}{len(df)}{S}")
    return t

@verbose
def tab_by(df, col, by):
    cb = {}
    for b in df[by].unique():
        print(f"{g}{by}: {G}{b}{S}")
        tab(df[df[by] == b], col)
        cb[b] = tab(df[df[by] == b], col)
    return cb

@verbose
def tab_race(df, col = 'race'):
    ts = df[col].value_counts()
    n = df[col].value_counts(normalize=True) * 100 
    r = df[df[col].notna()][col].unique().tolist()
    cp = 0.0
    rb = {}
    for c in r:
        t = ts.get(c, 0)
        p = n.get(c, 0.0)
        cp += p
        rb[c] = (t, round(p, 1), round(cp, 1))
    rb['Total'] = len(df)
    return rb
