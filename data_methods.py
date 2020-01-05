"""
Data methods for extracting, transforming, and loading data with Python
"""
import os
from glob import iglob
import pandas as pd


def update_using_iterrows(target_df, source_df, common_field, fields_to_fill):
    """
    :param target_df: <pandas.DaaFrame> DataFrame to update
    :param source_df: <pandas.DataFrame: DataFrame with source values
    :param common_field: <str> The field that may have a common value between DataFrames
    :param fields_to_fill: Iterable (list, tuple, set, e.g) of field names to populate from
                           source_df to target_df
    :returns: None
    """
    for source_df_index, source_df_row in source_df.iterrows():
        for target_df_index, target_df_row in target_df.iterrows():
            if target_df_row[common_field] == source_df_row[common_field]:
                for field_to_fill in fields_to_fill:
                    target_df.at[target_df_index, field_to_fill] = source_df[field_to_fill]


def update_using_apply(target_df, source_df):
    pass


def update_using_indexing(df1, df2, common_index_value):
    # Updates values in df1 with values in df2
    df1.set_index(common_index_value, inplace=True)
    df1.update(df2.set_index(common_index_value))
    df1.reset_index()
    return df1

