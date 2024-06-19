import pandas as pd

from utils.setup import *
from utils.tabulate import tab, tab_by, tab_race
from utils.utils import f

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
Gg = "\033[0;38;5;240m"


@verbose
def risk(df, pool, outcome, col):
    R = df[df[col].notna()][col].unique().tolist()
    pc = tab_race(df[df[pool] == '1'], col)
    oc = tab_race(df[df[outcome] == '1'], col)
    rb = {}
    rb['Total'] = len(df[df[pool] == '1'])
    for r in R:
        k = f((oc[r][0] / pc[r][0])*100, 2)
        rb[r] = k
    return rb

@verbose
def risk_ratio(non_white_risk, white_risk):
    return (f(non_white_risk, 2), f(white_risk, 2), f(non_white_risk / white_risk, 2))

@verbose
def calculate_risk(df, cases_df, charged_df, race_col):
    o={}
    cases_df = cases_df.dropna(subset=[race_col])
    o['Cases'] = len(cases_df)
    c = cases_df[race_col].value_counts()
    n = cases_df[race_col].value_counts(normalize=True)
    cc = charged_df[race_col].value_counts()
    nc = charged_df[race_col].value_counts(normalize=True)
    o['Charged'] = len(charged_df)
    o['Percent Charged'] = o['Charged'] / o['Cases'] *100
    o['Percent Charged'] = f"{round(o['Percent Charged'], 2)}%"
    cpc = 0
    cph = 0
    fr = {}

    for race in race_col.unique():
        cc = c.get(race, 0)
        pc = round(n.get(race, 0), 4) * 100
        cpc += pc
        ch = cc.get(race, 0)
        ph = round(nc.get(race, 0), 4) * 100
        cph += ph
        risk = ch / cc if cc != 0 else 0
        fr[race] = risk

        o[race] = {
            'Cases': round(cc, 2),
            'Percent Cases': f"{round(pc, 2)}%",
            'Cumulative Percent Cases': f"{round(cpc, 2)}%",
            'Charged': round(ch, 2),
            'Percent Charged': f"{round(pc, 2)}%",
            'Cumulative Percent Charged': f"{round(cph, 2)}%",
            'Risk': round(risk, 2),
            'Risk Percent': f'{round(risk * 100, 2)}%',
            'Relative Risk': '',  
            'Relative Risk Percent': '', 
            'Risk Increase': '',  
        }
    br = fr.get('White', 1)
    for rc in race_col.unique():
        rr = fr[rc] / br if br != 0 else 999
        o[rc]['Relative Risk'] = round(rr, 2)  
        o[rc]['Relative Risk Percent'] = f"{round((rr) * 100, 2)}%"
        if rr >= 1:
            o[rc]['Risk Increase'] = f"{round((rr - 1) * 100, 2)}%"
        else:
            o[rc]['Risk Increase'] = f"{round((1 - rr) * 100, 2)}%"
    return o
