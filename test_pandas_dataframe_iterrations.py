import os
import time
import pytest
import pandas as pd
import cdf


@pytest.fixture(scope='function')
def dataframe():
    return cdf.csv_to_df()


# Fails 1:143 because _iter_gby_dict_compregension is fatser than 
# _iter_gby_list_comprehension 1 in 144 times.
@pytest.mark.xfail
@pytest.mark.parametrize('func,columns_expected,dict_vs_list', [
    ('_iter_gby_dict_comprehension', 'df.columns', False),
    ('_iter_gby_list_comprehension', 'df.columns', False),
    ('_iter_gby_list_comprehension', 'df.columns', True),
])
def test_iter_group_by(dataframe, func, columns_expected, dict_vs_list):
    """
    Performance test to test speeds of iterating through a groupby object
    """
    df = dataframe
    assert isinstance(df, pd.DataFrame)
    gby = df.groupby('Edition')

    def _iter_gby_for_loop(gby_obj):
        # iterates through groupby object
        # using a for loop
        for key, group in gby_obj:
            print(key)
            print(group.count)

    def _iter_gby_list_comprehension(gby_obj):
        # iterates through a groupby object
        # using a list comprehension
        _df = cdf.pd.concat([g for i, g in gby])
        return _df

    def _iter_gby_dict_comprehension(gby_obj):
        # iterates through a group object
        # using a dict comprehension
        _df = cdf.pd.concat({k: g for k, g in gby})
        return _df

    start_time_a = time.time()
    _ = _iter_gby_for_loop(gby)
    real_time_a = time.time() - start_time_a

    start_time_b = time.time()
    result_df = eval(func)(gby)
    real_time_b = time.time() - start_time_b

    assert real_time_a > real_time_b
    assert sorted(df.columns) == sorted(result_df.columns)

    if dict_vs_list:
        if 'list' in func:
            start_time_c = time.time()
            _ = eval(func)(gby)
            real_time_c = time.time() - start_time_c

            start_time_d = time.time()
            _ = _iter_gby_dict_comprehension(gby)
            real_time_d = time.time() - start_time_d
        elif 'dict' in func:
            start_time_c = time.time()
            _ = _iter_gby_list_comprehension(gby)
            real_time_c = time.time() - start_time_c

            start_time_d = time.time()
            _ = eval(func)(gby)
            real_time_d = time.time() - start_time_d
        else:
            raise ValueError('Func "%s" not valid when dict_vs_list is True' % func)
        
        assert real_time_d > real_time_c


def test_updating_dataframe_with_values_of_another_dataframe(dataframe):
    """
    This tests the speeds of updating one dataframe with values from 
    another dataframe. It uses iterrows/at, merge, and indexing
    """
    df = dataframe
    df1 = pd.DataFrame([[1896, None, None],
                        [1809, None, None],
                        [1987, None, None]], columns=['Edition', 'Athlete', 'Sport'])
    assert isinstance(df, pd.DataFrame) and isinstance(df1, pd.DataFrame)
    sample_athlete = 'HAJOS, Alfred'
    sample_sport = 'Aquatics'

    def _update_using_iterrows(_df1, _df2):
        # df1 = dataframe to update
        # _df2 = dataframe with source values
        for _df1_index, _df1_row in _df1.iterrows():
            athlete = None
            sport = None
            if _df1_row['Edition'] in _df2['Edition']:
                athlete = _df1_row['Athlete']
                sport = _df1_row['Sport']

            _df1.at[_df1_index, 'Athlete'] = athlete
            _df1.at[_df1_index, 'Sport'] = sport

    _update_using_iterrows(df1, df)
    raise ValueError(df1)

