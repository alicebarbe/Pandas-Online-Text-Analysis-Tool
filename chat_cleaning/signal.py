# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 20:54:49 2020

@author: alice
"""

import pandas as pd
import numpy as np

def get_recipient_ids(threaddf, riddf):
    """
    Get the recipient ids of the participants in a signal chat

    Args:
        df (pandas.Dataframe): dataframe of signal chat (either sms.csv or mms.csv df).
        riddf (pandas.Dataframe): dataframe of Recipient ids (from recipient.csv).

    Returns:
        riddict (dict): dictionary of recipient IDs to name.

    """
    # get unique recipient id's of the thread
    rids = threaddf['address'].unique()
    # find corresponding names in recipient list - get list of first names only
    firstnames = riddf.loc[rids, 'system_display_name'].str.split().str.get(0)
    riddict = dict(zip(rids, firstnames))
    return riddict


def process_signal_sms_chat(filepath, ridfilepath, my_name, thread, order, timezone):
    """
    Create a texts DataFrame from a Signal csv file (should be sms.csv), the
    export of the sms table in the export database.

    Args:
        filepath (str): filepath to sms csv file.
        ridfilepath (str): filepath to recipient csv file.
        my_name (str): my first name.
        thread (int): thread number of signal conversation.
        order (list): order of columns in exported file.
        timezone (str): user timezone at time of export.

    Returns:
        sdata (pandas.Dataframe): dataframe containing cleaned sms data.

    """
    # input raw csv file
    rawsignaldata = pd.read_csv(filepath, index_col=False)
    riddf = pd.read_csv(ridfilepath, index_col=False).set_index('_id')

    # keep only specific chat
    mask = rawsignaldata.loc[:, 'thread_id'] == thread
    sdata = rawsignaldata[mask]

    # get recipient id dictionary
    riddict = get_recipient_ids(sdata, riddf)

    # create new dataframe without useless columns
    sdata = sdata.loc[:, ['date_sent', 'address', 'protocol', 'type', 'body']]

    # transform date from int format to timestamp format
    sdata['date_sent'] = sdata.loc[:, 'date_sent'].map(
            lambda x: pd.Timestamp(x, unit='ms', tz=timezone)
                        .tz_localize(None))

    # remove buggy/empty messages
    # 10485780 is messages from YOU to ME; 10485783 is messages from ME to YOU
    # 23 is SMS (non signal) message from ME to You; 23 is messages from YOU to ME
    sdata.drop(sdata.index[(sdata['type'] != 10485783) &
                           (sdata['type'] != 10485780) &
                           (sdata['type'] != 20) &
                           (sdata['type'] != 23)].tolist(), inplace=True)

    # add sender name
    sdata['sender'] = None
    # for my name: when protocol is nan (normally is 31337 for signal or 0 for SMS)
    mymessages_mask = sdata['protocol'].map(np.isnan)
    sdata.loc[mymessages_mask, 'sender'] = my_name
    # replace others' names corresponding to recipient ID (address column)
    sdata.loc[~mymessages_mask, 'sender'] = sdata.loc[~mymessages_mask, 'address'].map(riddict)

    # add columns for consistency
    sdata['platform'] = 'signal'

    # reorder columns
    sdata = sdata[order]

    return sdata

def process_signal_mms_chat(filepath, ridfilepath, my_name, thread, order, timezone):
    """
    Create a texts DataFrame from a Signal csv file (should be mms.csv), the
    export of the mms table in the export database.

    Args:
        filepath (str): filepath to sms csv file.
        ridfilepath (str): filepath to recipient csv file.
        my_name (str): my first name.
        thread (int): thread number of signal conversation.
        order (list): order of columns in exported file.
        timezone (str): user timezone at time of export.

    Returns:
        sdata (pandas.Dataframe): dataframe containing cleaned mms data.

    """
    # input raw csv file
    rawsignaldata = pd.read_csv(filepath, index_col=False)
    riddf = pd.read_csv(ridfilepath, index_col=False).set_index('_id')

    # keep only specific chat
    mask = rawsignaldata.loc[:, 'thread_id'] == thread
    sdata = rawsignaldata[mask]

    # get recipient id dictionary
    riddict = get_recipient_ids(sdata, riddf)

    # create new dataframe without useless columns
    sdata = sdata.loc[:, ['date', 'address', 'm_type', 'msg_box', 'body']]

    # transform date from int format to timestamp format
    sdata['date_sent'] = sdata.loc[:, 'date'].map(
            lambda x: pd.Timestamp(x, unit='ms', tz=timezone)
                        .tz_localize(None))

    # remove buggy/empty messages
    # 10485780 is messages from YOU to ME; 10485783 is messages from ME to YOU
    sdata.drop(sdata.index[(sdata['msg_box'] != 10485783) &
                           (sdata['msg_box'] != 10485780) &
                           (sdata['msg_box'] != 20) &
                           (sdata['msg_box'] != 23)].tolist(), inplace=True)

    # replace null text bodies with a space
    sdata['body'] = sdata['body'].fillna(' ')

    # add sender name
    sdata['sender'] = None
    # for my name: when mtype is 128 (132 for others)
    mymessages_mask = sdata['m_type'] == 128
    sdata.loc[mymessages_mask, 'sender'] = my_name
    sdata.loc[~mymessages_mask, 'sender'] = sdata.loc[~mymessages_mask, 'address'].map(riddict)

    # add columns for consistency
    sdata['platform'] = 'signal'

    # reorder columns
    sdata = sdata[order]

    return sdata
