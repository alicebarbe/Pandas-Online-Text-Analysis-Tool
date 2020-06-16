# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 16:52:39 2019

@author: ABarbe
"""

import pandas as pd
from chat_cleaning.signal import process_signal_sms_chat, process_signal_mms_chat
from chat_cleaning.whatsapp import process_whatsapp_chat
from chat_cleaning.groupme import process_groupme_chat
from chat_cleaning.discord import process_discord_chat
from chat_cleaning.facebookmessenger import process_facebook_chat
from config import *

if __name__ == "__main__":
    data_list = []  # initialize list to contain data tables
    if all(x in globals() for x in
           ['SIGNAL_SMS_CSV', 'SIGNAL_MMS_CSV', 'SIGNAL_RECIPIENT_CSV']):
        data_list.append(process_signal_sms_chat(SIGNAL_SMS_CSV, SIGNAL_RECIPIENT_CSV, MY_NAME, THREAD, ORDER, TIMEZONE))
        data_list.append(process_signal_mms_chat(SIGNAL_MMS_CSV, SIGNAL_RECIPIENT_CSV, MY_NAME, THREAD, ORDER, TIMEZONE))
    if 'WHATSAPP_TXT' in globals():
        data_list.append(process_whatsapp_chat(WHATSAPP_TXT, ORDER, WHATSAPP_PSEUDOS))
    if 'GROUPME_JSON' in globals():
        data_list.append(process_groupme_chat(GROUPME_JSON, ORDER, TIMEZONE, GROUPME_PSEUDOS))
    if 'DISCORD_JSON' in globals():
        data_list.append(process_discord_chat(DISCORD_JSON, ORDER, TIMEZONE, DISCORD_PSEUDOS))
    if 'FB_FOLDER' in globals():
        data_list.append(process_facebook_chat(FB_FOLDER, ORDER, TIMEZONE))

    # merge all sources
    merged_data = pd.concat(data_list, ignore_index=True)

    merged_data['date_sent'] = merged_data['date_sent'].astype('datetime64')

    # mergesort is the only stable sort
    merged_data.sort_values(by=['date_sent'], inplace=True, kind='mergesort')

    # convert to csv
    merged_data.to_csv(LOADPATH, index=False, header=True,
                       date_format='%Y-%m-%d %H:%M:%S.%f')
