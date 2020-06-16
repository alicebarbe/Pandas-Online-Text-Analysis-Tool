# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 22:15:25 2019

@author: Daniel
"""

import time
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import plot
from text_summary import TextSummary
from file_utils import convert_raw_csv_types
from config import *


def plot_totals(ts_dict):
    """
    Plot the total statistics (number of words, number of texts) per person.

    Args:
        ts_dict (dict): {"PersonName": TextSummary for that person}.

    Returns:
        None. Opens plot.

    """
    total_attrs = ['texts', 'words']
    titles = ['Texts', 'Words']
    number_of_plots = len(total_attrs)
    fig = make_subplots(rows=number_of_plots, cols=1, shared_xaxes=False,
                        subplot_titles=(titles))

    for index in range(number_of_plots):
        for sender in list(COLORS.keys()):
            fig.append_trace(go.Bar(
                                    x=[titles[index]],
                                    y=[ts_dict[sender].count[total_attrs[index]]],
                                    name=sender,
                                    showlegend=True,
                                    marker_color=COLORS[sender]),
                             index+1, 1)

    fig.update_layout(width=600, height=400*number_of_plots, barmode='group')
    fig.update_yaxes(title_text='Total')

    plot(fig, auto_open=True)

def plot_convo_words(convos, names):
    """
    Scatter plot of number of words per conversation.

    Args:
        convos (list): list of conversation dictionaries (see TextSummary class).
        names (list): [person on x axis, person on y axis].

    Returns:
        None. Opens plot.

    """
    x = [c['words_by_person'][names[0]] for c in convos]
    y = [c['words_by_person'][names[1]] for c in convos]
    started = ['Started: {}'.format(c['start_time']) for c in convos] # hover text
    color = [np.log10(c['duration'].delta/60e9) for c in convos] # color data
    fig = go.Figure(
            data=go.Scatter(x=x,
                            y=y,
                            mode='markers',
                            text=started,
                            marker_color=color,
                            marker_colorscale='Jet',
                            marker_colorbar_title="Convo duration (min)",
                            marker_colorbar_tickvals=[0.5, 1, 1.5, 2, 2.5, 3],
                            marker_colorbar_ticktext=["3", "10", "30", "100", "300"]))

    fig.update_layout(title='Words per conversation',
                      xaxis_title=names[0],
                      yaxis_title=names[1],
                      yaxis_scaleanchor = "x",
                      yaxis_scaleratio = 1)
    fig.update_xaxes(type='log')
    fig.update_yaxes(type='log')
    plot(fig, auto_open=True)

def plot_convo_length(convos):
    """
    Scatter plot of number of words vs duration of conversations

    Args:
        convos (list): list of conversation dictionaries (see TextSummary class).

    Returns:
        None. Opens plot.

    """
    x = [c['duration'].delta/60e9 for c in convos]
    y = [c['total_words'] for c in convos]
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='markers'))
    fig.update_layout(title='Convo duration vs words',
                      xaxis_title="Duration (minutes)",
                      yaxis_title="Words",
                      yaxis_scaleanchor = "x",
                      yaxis_scaleratio = 1)
    fig.update_xaxes(type='log')
    fig.update_yaxes(type='log')
    plot(fig, auto_open=True)

if __name__ == "__main__":
    START_TIME = time.time()

    df = pd.read_csv(LOADPATH, index_col=False)
    df = convert_raw_csv_types(df)

    names = list(COLORS.keys())
    df_person_list = [df[df['sender'] == name] for name in names]
    summary_all = TextSummary(df)
    ts_dict = dict(zip(names, [TextSummary(df_person)
                               for df_person in df_person_list]))
    plot_totals(ts_dict)
    convos = summary_all.get_conversations(names)
    plot_convo_words(convos, names)
    plot_convo_length(convos)

    print("--- %s sec execution time ---" % (time.time() - START_TIME))
