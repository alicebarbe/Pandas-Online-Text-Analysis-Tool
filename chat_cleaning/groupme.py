# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:53:27 2020

@author: alice
"""

import pandas as pd

def process_groupme_chat(filepath, order, timezone, pseudos=None):
    """Create a texts DataFrame from a GroupMe json file.

    Arguments:
        filepath (str): filepath to groupme json file.
        order (list): order of columns in exported file.
        timezone (str): user timezone at time of export.

    Returns:
        gmdata (pandas.Dataframe): dataframe containing cleaned data.
    """

    # input raw json file
    groupmerawdata = pd.read_json(filepath)

    # keep only relevant columns
    gmdata = groupmerawdata.loc[:, ['created_at', 'name', 'text']]

    # reverse ORDER (groupme export is in reverse chronological ORDER)
    gmdata = gmdata.reindex(index=gmdata.index[::-1])

    # convert date to timestamp type:
    # localize to UTC to give the tz naive ts a timezone, convert to EST/EDT,
    # and make it tz naive again
    gmdata['date_sent'] = gmdata['created_at'].map(
            lambda x: x.tz_localize('UTC')
                       .tz_convert(timezone)
                       .tz_localize(None))

    # replace null text bodies with a space
    gmdata['text'] = gmdata['text'].fillna(' ')

    # add sender column
    gmdata['sender'] = gmdata['name'].str.split().str.get(0)
    if pseudos is not None:
        for name, pseudo in pseudos.items():
            gmdata['sender'] = gmdata['sender'].str.replace(pseudo, name)
    # remove GroupMe-generated messages (adding users to group, for example)
    gmdata.drop(gmdata[gmdata['sender'] == 'GroupMe'].index, inplace=True)

    # add extra columns and delete extra columns
    gmdata['platform'] = 'groupme'
    gmdata = gmdata.rename(columns={'text': 'body'})

    # add columns for consistency
    gmdata = gmdata[order]

    return gmdata
