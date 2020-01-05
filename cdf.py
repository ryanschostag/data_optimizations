"""
Module for converting csv files to dataframes
"""
import os
from glob import iglob
import pandas as pd


def csv_to_df(file='olympics.csv', skip=4):
    # Get sthe file to pass to pd.read_csv
    # and rerturns a pd.DataFrame of that file
    files = [i for i in iglob('**/*', recursive=True) if file in i]
    ocsv = files[0] if files else None
    print('ocsv: %s' % ocsv)
    if ocsv is not None:
        print('not none')
        return pd.read_csv(os.path.abspath(ocsv), skiprows=skip)
    else:
        print('none')
        return None

