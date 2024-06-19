
import json
import os

import pandas as pd

from utils.risk import calculate_risk
from utils.setup import *
from utils.tabulate import tab, tab_by, tab_race


@verbose
def calc_disparity(df):
    calc = {}
    pool = df[(df['187'] == 1) & (df['robberyPool'] == 1)].drop_duplicates(subset=['courtCase', 'personID']).reset_index(drop=True)
    calc['ROBBERY_TOTAL'] = len(df[df['robberyPool'] != 0])
    calc['ROBBERY_BY_RACE'] = tab_race(df[df['robberyPool'] != 0])
    calc['RRISK'] = calculate_risk(pool, pool, pool[pool['robberySpecial'] == 1], 'race') 
    calc['FIREARM_RRISK'] = calculate_risk(pool, pool[pool['weapon']=='Firearm'], pool[pool['robberySpecial'] == 1], 'race') 
    
    pool['felonyRecordAny'] = pool[['priorFelonyCount']].max(axis=1)
    calc['RECORD_RRISK'] = calculate_risk(pool, pool[pool['priorFelonyCount'] > 0], pool[pool['robberySpecial'] == 1], 'race')
    
    









