import os
import time
import pytest
import pandas as pd
import cdf
import data_methods as dm


@pytest.fixture(scope='function')
def olympics():
    return cdf.csv_to_df()


@pytest.fixture(scope='function')
def customers():
    # A dataset full of customers
    df = pd.read_csv('SalesJan2009.csv')
    ids = list(range(0, df.shape[0]))
    df['Customer_ID'] = ids
    return df


# Fails 1:143 because _iter_gby_dict_compregension is fatser than 
# _iter_gby_list_comprehension 1 in 144 times.
@pytest.mark.xfail
@pytest.mark.parametrize('func,columns_expected,dict_vs_list', [
    ('_iter_gby_dict_comprehension', 'df.columns', False),
    ('_iter_gby_list_comprehension', 'df.columns', False),
    ('_iter_gby_list_comprehension', 'df.columns', True),
])
def test_iter_group_by(olympics, func, columns_expected, dict_vs_list):
    """
    Performance test to test speeds of iterating through a groupby object
    """
    df = olympics
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


def test_update_using_iterrows(olympics):
    # tests that the dm.update_using_iterrows 
    # function works as expected
    df1 = pd.DataFrame([[1896, None, None],
                        [1900, None, None],
                        [2008, None, None]], columns=['Edition', 'Athlete', 'Sport'])
    _ = dm.update_using_iterrows(df1, olympics)
    assert sorted(df1.columns) == ['Athlete', 'Edition', 'Sport']
    assert df1.Athlete.notnull().all()
    assert df1.Edition.notnull().all()
    assert df1.Sport.notnull().all()


def test_updating_dataframe_with_values_of_another_dataframe(customers):
    """
    This tests the speeds of updating one dataframe with values from 
    another dataframe. It uses iterrows/at, merge, and indexing
    """
    df = customers
    df1 = pd.DataFrame([[1, None, None],
                        [20, None, None],
                        [30, None, None]], columns=['Customer_ID', 'Name', 'Sport'])
    iterrows_start = time.time()
    _ = dm.update_using_iterrows(df1, df)
    iterrows_total = time.time() - iterrows_start
    assert iterrows_total < 50

def test_customers_df(customers):
    # testing the customers fixture
    df = customers
    assert 'Customer_ID' in df.columns
   

