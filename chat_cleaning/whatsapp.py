# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:59:42 2020

@author: alice
"""

import pandas as pd
import regex


def process_whatsapp_chat(filepath, order, pseudos=None):
    """
    Create a texts DataFrame from a whatsapp txt file.

    Args:
        filepath (str): filepath to whatsapp txt file.
        order (list): order of columns in exported file

    Returns:
        wadata (pandas.Dataframe): dataframe containing cleaned data.

    """
    # some regex to account for messages taking up multiple lines
    regstr = r"(?<datetime>\d{1,2}\/\d{1,2}\/\d{1,4}, \d{1,2}:\d{1,2}( (?i)[ap]m)*) - (?<name>.(?::\+*\-*\s*\w+)*|[\w\s\+\-]+?)(?:\s+(?<action>joined|left|was removed|changed the (?:subject to \"\w+\"|group's icon))|:\s(?<message>(?:.+|\n(?!\d{1,2}\/\d{1,2}\/\d{1,4}, \d{1,2}:\d{1,2}( (?i)[ap]m)*))+))"

    with open(filepath) as f:
        file_string = f.read()

    wadata = pd.DataFrame(regex.findall(regstr, file_string))

    wadata.columns = ['date_sent', '', 'senderfull', '', 'body', '']

    # remove last names
    wadata['sender'] = wadata['senderfull'].str.split().str.get(0)
    if pseudos is not None:
        for name, pseudo in pseudos.items():
            wadata['sender'] = wadata['sender'].str.replace(pseudo, name)

    # drop now useless columns and blank rows
    wadata = wadata[~wadata['sender'].isna()]
    wadata = wadata.drop(columns=['senderfull', ''])

    # change date to timestamp format
    wadata['date_sent'] = wadata['date_sent'].map(pd.Timestamp)

    # create platform column
    wadata['platform'] = 'whatsapp'

    # replace <Media omitted> with blank space
    wadata = wadata.replace("<Media omitted>", " ")
    # remove "missed voice call" and "missed video call" tags
    wadata = wadata[wadata['body'] != 'Missed voice call']
    wadata = wadata[wadata['body'] != 'Missed video call']

    # reorder columns
    wadata = wadata[order]

    return wadata
