"""
Data methods for extracting, transforming, and loading data with Python
"""
import os
from glob import iglob
import pandas as pd


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


def update_using_indexing(df1, df2, common_index_value):
    # Updates values in df1 with values in df2
    df1.set_index(common_index_value, inplace=True)
    df1.update(df2.set_index(common_index_value))
    df1.reset_index()
    return df1

