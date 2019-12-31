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


def update_using_iterrows(target_df, source_df):
    # df1 = dataframe to update
    # source_df = dataframe with source values
    for source_df_index, source_df_row in source_df.iterrows():
        for target_df_index, target_df_row in target_df.iterrows():
            if target_df_row['Edition'] == source_df_row['Edition']:
                if  not target_df_row['Athlete'] and not target_df_row['Sport']:
                    athlete = source_df_row['Athlete']
                    sport = source_df_row['Sport']
    
                    target_df.at[target_df_index, 'Athlete'] = athlete
                    target_df.at[target_df_index, 'Sport'] = sport


def update_using_apply(target_df, source_df):
    # Update values in target_df with values of 
    # source_df
    def _update_values(df):
        pass


