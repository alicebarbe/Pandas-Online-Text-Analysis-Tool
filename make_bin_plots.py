# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 08:51:26 2019

@author: Alice

"""

import time
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot
from file_utils import convert_raw_csv_types
from text_summary_list_utils import create_list_of_summaries_by_person,\
    make_attribute_dict, make_occurrence_dict
from config import COLORS, LOADPATH, BIN_FREQ, TOKEN_LIST


def make_area_plots(indices, dict_of_attribute_dicts, filename):
    """
    Make filled area plots of the lists in attribute_dicts, divided by person.

    Args:
        indices (list): list of timestamps
        dict_of_attribute_dicts (dict): {key = name of person, value = attribute_dict}
        filename (str): filename of html file

    Returns:
        None. Opens the plot automagically.
    """
    list_of_plots = []
    titles = []
    # list of min and maxs of y axis range
    mins_y = []
    maxs_y = []
    # for each person
    for person_name in dict_of_attribute_dicts:
        attribute_dict = dict_of_attribute_dicts[person_name]
        color = COLORS[person_name]
        person_plots = []  # list of subplots for each person

        # for each attribute dict item, which are values of the attribute dict,
        # which itself is the value of the name attribute dict pair
        showlegend = True
        for title in attribute_dict:
            # create list of titles
            titles.append(title)
            # replace nans with zeros in attribute list
            y = [0 if np.isnan(e) else e for e in attribute_dict[title]]
            # find y limits
            mins_y.append(min(y))
            maxs_y.append(max(y))
            person_plots.append(go.Scatter(name=person_name,
                                           x=indices,
                                           y=y,
                                           fill='tozeroy',
                                           line_color=color,
                                           legendgroup=person_name,
                                           showlegend=showlegend))
            # don't duplicate the legend after the first plot
            showlegend = False

        # append the list of plots for a person to a master list of plots
        list_of_plots.append(person_plots)

    # number of plots, determined by the length of an attribute_dict
    number_of_plots = len(list(dict_of_attribute_dicts.values())[0])

    # initialize subplot figure
    fig = make_subplots(rows=number_of_plots, cols=1, shared_xaxes=True,
                        subplot_titles=(titles))

    # get most extreme y limits per plot
    rows = len(dict_of_attribute_dicts)
    cols = len(mins_y)//rows
    y_ax_mins = np.reshape(mins_y, [rows, cols]).min(axis=0)
    y_ax_maxs = np.reshape(maxs_y, [rows, cols]).max(axis=0)


    # create "matrix" of subplots by appending their trace
    for person_plots in list_of_plots:
        for subplot_num in range(len(person_plots)):
            subplot = person_plots[subplot_num]
            fig.append_trace(subplot, subplot_num+1, 1)
            fig.update_yaxes(row=subplot_num+1, col=1,
                             range=[y_ax_mins[subplot_num],
                                    1.05*y_ax_maxs[subplot_num]])

    fig.update_layout(width=1200, height=max(200*number_of_plots, 300))

    plot(fig, auto_open=True, filename=filename)


if __name__ == "__main__":
    START_TIME = time.time()

    df = pd.read_csv(LOADPATH, index_col=False)
    df = convert_raw_csv_types(df)

    # create bins and groups
    df['shifted'] = df['date_sent']-pd.Timedelta(hours=5)
    grouper1d = pd.Grouper(key='shifted', freq=BIN_FREQ)

    names = list(COLORS.keys())

    dfs_group1d = df.groupby(grouper1d)

    # get indices of the bins
    bin_indices = list(dfs_group1d.groups.keys())

    # create textsummary lists
    text_summaries_list = create_list_of_summaries_by_person(dfs_group1d, names)

    # create attribute dictionaries to plot
    name_attr_dict_pairs = dict(zip(names, [make_attribute_dict(text_summaries)
                                            for text_summaries in text_summaries_list]))

    # create area plots
    make_area_plots(bin_indices, name_attr_dict_pairs, "Area Plot.html")

    if len(TOKEN_LIST) > 0:
        # create word frequency dictionaries to plot
        name_occ_dict_pairs = dict(zip(names, [make_occurrence_dict(text_summaries, TOKEN_LIST)
                                               for text_summaries in text_summaries_list]))

        # create area plots
        make_area_plots(bin_indices, name_occ_dict_pairs, "Token Area Plots.html")

    print("--- %s sec execution time ---" % (time.time() - START_TIME))
