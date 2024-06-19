from collections import Counter

import pandas as pd

from utils.setup import *


@verbose()
def list_counter(df, column, dropna=True, drop_low_freq=False, low_freq=20):
    if dropna:
        df = df.dropna(subset=[column])
    f = [i for sl in df[column] for i in sl]
    oc = Counter(f)
    nac = Counter()
    for sl in df[column]:
        if len(sl) > 1:
            for i in sl[1:]:
                nac[i] += 1
    ocd = pd.DataFrame.from_dict(oc, orient='index', columns=['Count'])
    ndf = pd.DataFrame.from_dict(nac, orient='index', columns=['Not_Arr'])
    ocd.reset_index(inplace=True)
    ndf.reset_index(inplace=True)
    ocd.columns = [column, 'Count']
    ndf.columns = [column, 'Not_Arr']
    rdf = pd.merge(ocd, ndf, on=column, how='left').fillna(0)
    if drop_low_freq:
        rdf = rdf[rdf['Not_Arr'] >= low_freq]
    return rdf