# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 22:00:59 2019

@author: Daniel
"""

import pandas as pd

def convert_raw_csv_types(data):
    """Converts string representations of dates of our standard input dataframe
    from the CSV to timestamps and returns the dataframe. Converts all message
    content to strings.

    Args:
        data (Pandas.DataFrame): raw import converted to CSV.

    Returns:
        data (Pandas.DataFrame): import with timestamps converted to the correct type.
    """
    data['date_sent'] = data['date_sent'].map(pd.Timestamp)
    data['body'] = data['body'].map(str)
    return data
