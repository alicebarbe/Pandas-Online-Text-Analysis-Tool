# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:49:06 2020

@author: alice
"""

import time
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot
from text_summary import TextSummary
from file_utils import convert_raw_csv_types
from config import LOADPATH, COLORS


def make_scatter_plots(text_summary_by_person):
    """
    Create scatter plot of ratio of each person's usage of words

    Args:
        text_summary_by_person (dict): {"Person1": TextSummary for that person, etc.}.

    Returns:
        None. Opens plot.

    """

    MIN_WORD_OCCUR = 10  # minimum number of occurrences to be plotted
    MIN_EMOTE_OCCUR = 5

    names = list(COLORS.keys())

    diffs = dict()  # stores dictionaries with key word and value (total, ratio)

    # make dictionaries
    diffs['words'] = text_summary_by_person[0].compare_freq(text_summary_by_person[1], 'words')
    diffs['emotes'] = text_summary_by_person[0].compare_freq(text_summary_by_person[1], 'emotes')

    # strip less frequent tokens
    diffs['words'] = {key: value for (key, value) in diffs['words'].items() if
                      value[0] >= MIN_WORD_OCCUR}
    diffs['emotes'] = {key: value for (key, value) in diffs['emotes'].items() if
                       value[0] >= MIN_EMOTE_OCCUR}

    number_of_plots = 2
    titles = ['Words', 'Emotes']

    # initialize subplot figure
    fig = make_subplots(rows=number_of_plots, cols=1, shared_xaxes=True,
                        subplot_titles=(titles))

    subplot = 0
    for token_type, diff_dict in diffs.items():

        x, y, customdata = [], [], []
        for word, v in diff_dict.items():
            y.append(v[0])
            x.append(v[1])
            customdata.append([word, names[0], v[2], names[1], v[3]])

        fig.append_trace(go.Scatter(x=x,
                                    y=y,
                                    customdata=customdata,
                                    hovertemplate="<b>%{customdata[0]}</b><br>" +\
                                                  "Total: %{y} <br>Ratio: %{x:.2f}<br>" +\
                                                  "%{customdata[1]}: %{customdata[2]}<br>" +\
                                                  "%{customdata[3]}: %{customdata[4]}<extra></extra>",
                                    showlegend=False,
                                    mode='markers'),
                         subplot+1, 1)
        subplot += 1

    fig.update_layout(width=1200, height=600*number_of_plots)
    fig.update_xaxes(type='log', title_text=f'{names[0]}: {names[1]} ratio')
    fig.update_yaxes(type='log', title_text='Total')

    plot(fig, auto_open=True, filename="Word Ratio Scatterplot.html")


if __name__ == "__main__":
    START_TIME = time.time()

    df = pd.read_csv(LOADPATH, index_col=False)
    df = convert_raw_csv_types(df)

    names = list(COLORS.keys())

    # create comparison scatter plot
    text_summary_by_person = [TextSummary(df[df['sender'] == name]) for name in names]
    make_scatter_plots(text_summary_by_person)

    print("--- %s sec execution time ---" % (time.time() - START_TIME))
