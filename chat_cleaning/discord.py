# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:05:19 2020

@author: alice
"""

import pandas as pd
import json

def process_discord_chat(filepath, order, timezone, pseudos=None):
    """Create a texts DataFrame from a Discord json file.

    Arguments:
        filepath (str): filepath to discord json file.
        order (list): order of columns in exported file.
        timezone (str): user timezone at time of export.
        pseudos (dict): dictionary of real names to discord names of form {'name': 'handle'}.

    Returns:
        ddata (pandas.Dataframe): dataframe containing cleaned data.
    """

    # input raw json file
    f = open(filepath)
    fjson = json.load(f)
    f.close()
    drawdata = pd.DataFrame(fjson['messages'])

    # keep only relevant columns
    ddata = drawdata.loc[:, ['timestamp', 'author', 'content']]

    # convert date to timestamp type:
    # convert to EST/EDT and make it tz naive again
    ddata['date_sent'] = pd.to_datetime(ddata['timestamp'])
    ddata['date_sent'] = ddata['date_sent'].map(
            lambda x: x.tz_convert(timezone)
                       .tz_localize(None))

    # replace null text bodies with a space
    ddata['body'] = ddata['content'].fillna(' ')

    # add sender column
    ddata['sender'] = ddata['author'].apply(lambda x: x['name'])
    if pseudos is not None:
        for name, pseudo in pseudos.items():
            ddata['sender'] = ddata['sender'].str.replace(pseudo, name)

    # add extra columns and delete extra columns
    ddata['platform'] = 'discord'
    ddata = ddata.reset_index()

    # add columns for consistency
    ddata = ddata[order]

    return ddata
