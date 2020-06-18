# -*- coding: utf-8 -*-
"""
Created on Tue May 19 22:22:39 2020

@author: alice
"""

import yaml
import pandas as pd
from plotly.colors import DEFAULT_PLOTLY_COLORS

# initialize a few variables to None in case they are not defined in config.txt
DISCORD_PSEUDOS = None
WHATSAPP_PSEUDOS = None
GROUPME_PSEUDOS = None
TOKEN_LIST = []
TIMEZONE = 'US/Eastern'  # default timezone is US Eastern

# binned plot settings
BIN_FREQ = '1d'

# heatmap plot settings
BIN_FREQ_HM = '1h'
BIN_FREQ2 = 24

# initialize order
ORDER = ['date_sent', 'platform', 'sender', 'body']

# open configuration file and load its variables globally
with open('config/config.txt', 'r') as configfile:
    config = configfile.read()
config_dict = yaml.safe_load(config)
globals().update(config_dict)

# test if colors are defined - if not, get list of names and assign them colors
try:
    df = pd.read_csv(LOADPATH, index_col=False)
    if 'OFFSET' not in globals():
        # find offset: used in heatmap to displace first point. Default here
        # to hour of first text
        OFFSET = int(df.loc[0, 'date_sent'][11:13])
    if 'COLORS' not in globals():
        names = list(df['sender'].unique())
        colors = DEFAULT_PLOTLY_COLORS[0:len(names)]
        COLORS = dict(zip(names, colors))
except:
    print("Warning: LOADFILE has not been created yet. COLORS failed to be defined.")

