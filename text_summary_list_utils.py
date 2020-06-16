# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 16:19:43 2020

@author: alice
"""

from text_summary import TextSummary

def create_list_of_summaries(data_groups):
    """Create a list of text summaries from a dataframe groupby object
    Arguments:
        data_groups (Pandas.GroupBy):
            groupby object with data grouped by time
    Returns:
        text_summary_list (list of TextSummary):
            list of TextSummary objects for each bin
    """
    text_summary_list = []
    for i in range(len(data_groups.size())):
        # for non-empty bins
        if data_groups.size()[i] != 0:
            # get dataframe for the given selected group and construct a
            # TextSummary from it
            dataframe = data_groups.get_group(data_groups.size().index[i])
            text_summary_list.append(TextSummary(dataframe))
        else:
            # for empty bins, construct a blank TextSummary
            text_summary_list.append(TextSummary())
    return text_summary_list


def create_list_of_summaries_by_person(data_groups, names):
    """Same as create_list_of_summaries except divided by person - so one
    list per person packaged together in a big list.
    """
    text_summary_list_of_lists = []
    for name in names:
        text_summary_list = []
        for i in range(len(data_groups.size())):
            # for non-empty bins
            if data_groups.size()[i] != 0:
                # get dataframe for the given selected group and construct a
                # TextSummary from it
                dataframe = data_groups.get_group(data_groups.size().index[i])
                # filter by name
                dataframe = dataframe[dataframe['sender'] == name]
                text_summary_list.append(TextSummary(dataframe))
            else:
                # for empty bins, construct a blank TextSummary
                text_summary_list.append(TextSummary())
        text_summary_list_of_lists.append(text_summary_list)
    return text_summary_list_of_lists


def get_summary_attribute_list(text_summary_list, attribute, key):
    """Get a list of a dictionary value in an attribute from a list of
    TextSummaries
    Arguments:
        text_summary_list (list of TextSummary):
            list of TextSummary objects
        attribute (str):
            string of the dictionary attribute name
        key (str):
            string of the dictionary key value to get
    Return:
        attribute_list (list):
            list of the values assigned to *key* in *attribute* for each
            TextSummary
    """
    attribute_list = []
    for text_summary in text_summary_list:
        attribute_list.append(getattr(text_summary, attribute).get(key))
    return attribute_list


def make_attribute_dict(summary_list):
    """Returns a list of the things to plot given a list of textSummaries.
    Add new things to plot per bins here!
    Arguments:
        summary_list (list of TextSummary)
    Returns:
        attribute_dict (dictionary of lists of ints/floats):
            key = title of the plot
            value = list of the values
    """
    attribute_dict = dict()
    attribute_dict['Number of Texts'] = \
        get_summary_attribute_list(summary_list, 'count', 'texts')
    attribute_dict['Number of Emoji'] = \
        get_summary_attribute_list(summary_list, 'count', 'emotes')
    attribute_dict['Number of Characters'] = \
        get_summary_attribute_list(summary_list, 'count', 'chars')
    attribute_dict['Words per Text'] = \
        get_summary_attribute_list(summary_list, 'prop', 'words_per_text')
    attribute_dict['Laziness'] = \
        get_summary_attribute_list(summary_list, 'prop', 'laziness')
    attribute_dict['Percent of Emoji'] = \
        get_summary_attribute_list(summary_list, 'prop', 'percent_emote')
    attribute_dict['Verbosity'] = \
        get_summary_attribute_list(summary_list, 'prop', 'verbosity')
        
    return attribute_dict

def make_occurrence_dict(summary_list, token_list):
    """Returns a dictionary of the list of occurrence of tokens for each TextSummary
    in a list of TextSummaries.

    Args:
        summary_list (list): list of TextSummaries.
        token_list (list): list of tokens, strings, to search for.

    Returns:
        occurrence_dict (dict): {"token": [occurrence of token in each textSummary}.
    """
    occurrence_dict = dict()
    for token in token_list:
        occurrence_dict[token] = [summary.occurrence_dicts['words'].get(token, 0) +
                                  summary.occurrence_dicts['emotes'].get(token, 0)
                                  for summary in summary_list]
    return occurrence_dict
