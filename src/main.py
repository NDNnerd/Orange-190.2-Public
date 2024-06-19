import json
import os

import pandas as pd

from charge_descriptives import charge_descriptives
from descriptive_table import global_out, table_cat, table_cont
from disparity_calc import disparity_calc
from fetch import fetch_data
from homicide_descriptives import homicide_descriptives
from per_dis import calc_app_count
from utils.risk import calculate_risk
from utils.setup import *

pd.set_option('display.max_columns', None)
import dotenv

dotenv.load_dotenv()

@verbose
def main():
    county = {
        "San Bernardino": "Neighbor",
        "Riverside": "Neighbor",
        "Orange": "Main",
        "Los Angeles": "Neighbor",
        "San Diego": "Neighbor"
    }

    with open('query_config.json') as f:
        query_config = json.load(f)

    df = pd.DataFrame()
    for query in query_config:
        data = fetch_data(f"SELECT * FROM charges WHERE {query['charge']}")
        data['robberyPool'] = query['pool']
        data['robberySpecial'] = query['rspecial']
        df = pd.concat([df, data])
        
    with open('Results.json', 'w') as f:
        json.dump(homicide_descriptives(df), f)
    with open('Results.json', 'a') as f:
        json.dump(charge_descriptives(df), f)
    with open('Results.json', 'a') as f:
        json.dump(disparity_calc(df), f)

    s = table_cont(df, ['courtCase', 'personID', 'special', 'defendantID', 'countID'])
    s.to_csv('table_cont.csv')
    t = table_cat(df, ['sex', 'nCharges', 'homicideCount', 'dispo', 'nSuspects', 'nVictims','sexVictim', 'raceVictim', 'ageVictimGroup', 'raceEqualsVrace','location', 'weapon', 'event', 'spCirc', 'relation1', 'priorFelony', 'strike', 'felonyRecord', 'fullRecord'])
    t.to_csv('table_cat.csv')

    df['countyResidence'] = df['countyResidence'].map(lambda x: county.get(x, "Other"))
    place = {}
    for p in df['countyResidence'].unique():
        place[p + '_R'] = calculate_risk(df, df[df['countyResidence']=='p'], df[df['robberySpecial'] == 1], 'race')
        place[p] = calculate_risk(df, df[df['countyResidence']=='p'], df[df['robberySpecial'] == 1], 'race')

    dda = fetch_data(f"SELECT * FROM charges WHERE charges LIKE '%187(a)%' AND race IN ('Black', 'White')")
    dda['special'] = dda['charges'].apply(lambda x: 1 if any('190.2' in charge for charge in x) else 0)
    dda = dda.explode('DDA')
    dda = calc_app_count(dda, 'DDA', 'special')
    dda_df = pd.DataFrame(dda)
    dda_df.to_csv('DDA.csv')
    
if __name__ == "__main__":
    main()