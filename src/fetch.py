
import json
import os

import pandas as pd

from utils.setup import *
from utils.tabulate import tab_race


@verbose
def homicide_descriptives(df):
    homicide = {}
    h = df[df['187'] == 1].drop_duplicates(subset=['courtCase', 'countID', 'personID'])
    homicide['HOMICIDE_BY_RACE'] = tab_race(h)
    homicide['HOMICIDE_COUNTS'] = len(h.assign(homicideCountID=lambda x: x['courtCase'] + x['countID'].astype(str))['homicideCountID'].unique())
    h['personHomicideCount'] = h.groupby('defCaseID')['187'].transform('sum')
    homicide['PERSONS_WITH_MULTIPLE_HOMICIDES'] = len(h[h['personHomicideCount'] > 1])
    homicide['MULTIPLE_HOMICIDES_RACE'] = tab_race(h[h['personHomicideCount'] > 1])
    return homicide

