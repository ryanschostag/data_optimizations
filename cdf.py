"""
Module for converting csv files to dataframes
"""
import os
from glob import iglob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


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


def save_plot(pandas_series, output_path='./my_plot.png'):
    # takes a pandas.Series, plots it,
    # and saves a png of the plot
    # If the series has a pandas.Series.name, it will print
    # Returns the fig object
    fig = plt.figure()
    _ = fig.add_subplot(pandas_series.plot())
    _ = fig.savefig(output_path)
    print('pandas.Series.name of "%s" plotted and saved to "%s"' % (pandas_series.name, output_path))
    return fig

