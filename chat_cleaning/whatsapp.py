# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:59:42 2020

@author: alice
"""

import pandas as pd


def process_whatsapp_chat(filepath, order, pseudos=None):
    """
    Create a texts DataFrame from a whatsapp txt file.

    Args:
        filepath (str): filepath to whatsapp txt file.
        order (list): order of columns in exported file

    Returns:
        wadata (pandas.Dataframe): dataframe containing cleaned data.

    """
    # input raw whatsapp text file
    warawdata = pd.read_csv(filepath, sep='\n', header=None, index_col=False,
                            engine='python')
    warawdata.columns = ['line']

    # eliminate non actual messages - real messages have colons
    wadata = warawdata.loc[warawdata['line'].str.count(':') >= 2, :]
    # split date
    wadata[['date_sent', 'body']] = wadata['line'].str.split(r' - ', 1, expand=True)
    wadata[['senderfull', 'body']] = wadata['body'].str.split(r': ', 1, expand=True)
    # remove last names
    wadata['sender'] = wadata['senderfull'].str.split().str.get(0)
    if pseudos is not None:
        for name, pseudo in pseudos.items():
            wadata['sender'] = wadata['sender'].str.replace(pseudo, name)

    # drop now useless columns and blank rows
    wadata = wadata[~wadata['sender'].isna()]
    wadata = wadata.drop(columns=['line', 'senderfull'])

    # change date to timestamp format
    wadata['date_sent'] = wadata['date_sent'].map(pd.Timestamp)

    # create platform column
    wadata['platform'] = 'whatsapp'

    # replace <Media omitted> with blank space
    image_mask = wadata['body'] == "<Media omitted>"
    wadata = wadata.replace("<Media omitted>", " ")

    # reorder columns
    wadata = wadata[order]

    return wadata
