# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:33:52 2020

@author: alice
"""

import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import plot
from file_utils import convert_raw_csv_types
from text_summary_list_utils import create_list_of_summaries,\
    make_attribute_dict, make_occurrence_dict
from config import *


def make_heatmap_plot(dates, attribute_dict, title):
    """
    Make heatmap plot of the attribute in attribute_dict over time, presumably
    hours on xaxis, days on yaxis.

    Args:
        dates (list): list of timestamps for each datapoint.
        attribute_dict (dict): dictionary of attributes of form
            {'Attribute Name': list of the attribute over time}.
        title (str): title of heatmap plot, same as Attribute Name.

    Returns:
        None. Opens plot.

    """
    # calculate offset to pad the end
    end_offset = BIN_FREQ2 - (len(dates) + OFFSET)%BIN_FREQ2

    # calculate offsets and create date list
    index_start_offset = OFFSET * pd.Timedelta(BIN_FREQ_HM)
    index_end_offset = end_offset * pd.Timedelta(BIN_FREQ_HM)
    indices = pd.date_range(start=(min(dates) - index_start_offset),
                            end=(max(dates) + index_end_offset),
                            freq=(BIN_FREQ_HM))

    attribute_list = attribute_dict[title]

    fig = go.Figure()

    # pad beginning and end of attribute list
    zdata = ([0] * OFFSET) + attribute_list + ([0] * end_offset)
    # reshape to heatmap size
    zdata = np.reshape(zdata, (len(zdata)//BIN_FREQ2, BIN_FREQ2))

    color0 = px.colors.sequential.tempo[0]
    colorend = px.colors.sequential.tempo[-5]

    # create heatmap
    fig.add_trace(go.Heatmap(z=zdata,
                             y=indices[0:-1:BIN_FREQ2],
                             colorscale='tempo',
                             yaxis='y'))

    # add marginal graph above
    fig.add_trace(go.Bar(y=np.sum(zdata, axis=0), yaxis='y2',
                         marker_color=np.sum(zdata, axis=0),
                         marker_colorscale='tempo'))

    fig.add_trace(go.Bar(x=np.sum(zdata, axis=1), y=indices[0:-1:BIN_FREQ2],
                         marker_color=np.sum(zdata, axis=1),
                         marker_colorscale='tempo',
                         orientation='h', xaxis='x2', yaxis='y'))

    fig.update_layout(
        title_text=title,
        xaxis_title_text='Time of Day',
        plot_bgcolor=color0,
        autosize=False,
        yaxis_domain = [0,0.85],
        yaxis2 = dict(domain = [0.85,1]),
        xaxis_domain = [0,0.85],
        xaxis2 = dict(domain = [0.85,1]),
        height = 800,
        hovermode = 'closest',
        showlegend = False)

    plot(fig, auto_open=True)


if __name__ == "__main__":
    START_TIME = time.time()

    df = pd.read_csv(LOADPATH, index_col=False)
    df = convert_raw_csv_types(df)

    # create bins and groups
    df['shifted'] = df['date_sent']-pd.Timedelta(hours=5)
    grouper1d = pd.Grouper(key='shifted', freq=BIN_FREQ_HM)

    df_group1d = df.groupby(grouper1d)

    # get indices of the bins
    bin_indices = list(df_group1d.groups.keys())

    # create textsummary lists
    text_summaries = create_list_of_summaries(df_group1d)

    # create attribute dictionaries to plot
    attr_dict = make_attribute_dict(text_summaries)

    # create heatmap plot
    make_heatmap_plot(bin_indices, attr_dict, 'Number of Texts')
    make_heatmap_plot(bin_indices, attr_dict, 'Number of Emoji')

    if len(TOKEN_LIST) > 0:
        # create word frequency dictionaries to plot
        occ_dict = make_occurrence_dict(text_summaries, TOKEN_LIST)
    
        # create heatmap plot
        for token in TOKEN_LIST:
            make_heatmap_plot(bin_indices, occ_dict, token)

    print("--- %s sec execution time ---" % (time.time() - START_TIME))
