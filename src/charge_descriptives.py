
import json
import os

import pandas as pd

from utils.setup import *
from utils.tabulate import tab, tab_by


@verbose
def charge_descriptives(df):
    charge = {}
    ct = df.drop_duplicates(subset=['courtCase', 'personID', 'countID'], keep='first')
    ct['personSpecialCount'] = ct.groupby('defCaseID')['special'].transform('sum')
    charge['SPECIAL_CIRCUMSTANCES'] = len(ct[ct['personSpecialCount'] > 0])
    ct['personCount'] = ct.groupby('defCaseID').transform('sum')
    charge['DEFENDANTS'] = len(ct[ct['personCount']  > 0])
    ct['personIncidentCount'] = ct.groupby('personID')['incidentID'].transform('nunique') - 1
    charge['PERSONS_WITH_MULTIPLE_INCIDENTS'] = len(ct[ct['personIncidentCount'] > 1]['defCaseID'].unique())
    charge['MATCHED_SHR'] = len(ct[ct['shr_matchCase'] == 1]) / len(ct)
    charge['MATCHED_SHR'] = round(charge['MATCHED_SHR'] * 100, 1)
    charge['UNMATCHED_SHR'] = len(ct[ct['shr_matchCase'] == 0]) / len(ct)
    charge['UNMATCHED_SHR'] = round(charge['UNMATCHED_SHR'] * 100, 1)
    charge['MATCHED_SHR'] = f"{charge['MATCHED_SHR']}%"
    charge['UNMATCHED_SHR'] = f"{charge['UNMATCHED_SHR']}%"
    charge['MATCHED_SHR_BY_RACE'] = tab_by(ct, 'shr_matchCase', 'race')
    charge['SHR_LOCATION'] = tab(ct, 'location')
    charge['SHR_WEAPON'] = tab(ct, 'weapon')
    charge['SHR_WEAPON_BY_RACE'] = tab_by(ct, 'weapon', 'race')
    charge['SHR_EVENT'] = tab(ct, 'event')
    charge['SHR_SPCIRCUM'] = tab(ct,'spCirc')
    return charge