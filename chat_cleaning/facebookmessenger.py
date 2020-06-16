# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 14:13:52 2020

@author: alice
"""

import pandas as pd
import json
from pathlib import Path

def process_facebook_json(filepath, order, timezone):
    """Create a texts DataFrame from a Facebook Messenger json file.

    Arguments:
        filepath (str): filepath to fbmessenger json file.
        order (list): order of columns in exported file.
        timezone (str): user timezone at time of export.

    Returns:
        fbdata (pandas.Dataframe): dataframe containing cleaned data.
    """

    # input raw json file
    f = open(filepath)
    fjson = json.load(f)
    f.close()
    fbrawdata = pd.DataFrame(fjson['messages'])

    # keep only relevant columns
    fbdata = fbrawdata.loc[:, ['timestamp_ms', 'sender_name', 'content']]

    # reverse ORDER (facebook export is in reverse chronological ORDER)
    fbdata = fbdata.reindex(index=fbdata.index[::-1])

    # convert date to timestamp type:
    # localize to UTC to give the tz naive ts a timezone, convert to EST/EDT,
    # and make it tz naive again
    fbdata['date_sent'] = pd.to_datetime(fbdata['timestamp_ms'], unit='ms')
    fbdata['date_sent'] = fbdata['date_sent'].map(
            lambda x: x.tz_localize('UTC')
                       .tz_convert(timezone)
                       .tz_localize(None))

    # replace null text bodies with a space
    fbdata['text'] = fbdata['content'].fillna(' ')

    # add sender column
    fbdata['sender'] = fbdata['sender_name'].str.split().str.get(0)

    # add extra columns and delete extra columns
    fbdata['platform'] = 'fbmessenger'
    fbdata = fbdata.rename(columns={'text': 'body'})
    fbdata = fbdata.reset_index()

    # add columns for consistency
    fbdata = fbdata[order]

    return fbdata


def process_facebook_chat(filepath, order, timezone):
    """Create a texts DataFrame from all the Facebook Messenger json file in a
    designated folder.

    Args:
        filepath (str): folder with facebook chats.
        order (list): order of columns in exported file.
        timezone (str): user timezone at time of export.

    Returns:
        fbdata (pandas.Dataframe): dataframe containing cleaned data.
    """
    fb_data_list = []
    paths = Path(filepath).glob('**/*.json')
    for path in paths:
        fb_data_list.append(process_facebook_json(path, order, timezone))
    fb_data = pd.concat(fb_data_list, ignore_index=True, sort=False)
    fb_data = fb_data[order].sort_values('date_sent').reset_index(drop=True)
    return fb_data
