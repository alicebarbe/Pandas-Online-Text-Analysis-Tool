# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 19:56:19 2019

@author: Daniel
"""

import time
import string
import pandas as pd
import numpy as np
from rake_nltk import Rake
from string_utils import count_word_occurrences, get_words, \
    remove_emotes, count_emotes, count_emote_occurrences
from file_utils import convert_raw_csv_types
from stat_utils import ratio_conf_bounds
from config import LOADPATH, COLORS

class TextSummary:
    """A representation of the basic statistics of a set of texts.

    Attributes:
        data (Pandas.DataFrame):
            input dataframe of texts
        count (dict):
            Number of _, has keys texts, words, char, space letter, digit,
            emotes, punct.
        prop (dict):
            contains overall statistics that are fractions
            (laziness, % of emoji, words per text, verbosity)
        occurrence_dicts (dict):
            contains dictionaries {token: count} (words or emotes)
        per_text_lists (dict):
            contains statistics per text
            (sentiment: polarity, subjectivity, words per text, characters per
            text, emotes per text)
    """

    def __init__(self, data=None):
        """Create a new TextSummary from the texts dataframe.

        Args:
            data (Pandas.DataFrame): texts dataframe, containing a 'body' column.

        """
        if data is None or data.empty:
            self.count = {'texts': 0, 'words': 0, 'chars': 0, 'spaces': 0,
                          'letters': 0, 'digits': 0, 'emotes': 0, 'punct': 0}
            self.prop = {'words_per_text': float('nan'), 'laziness': float('nan'),
                         'percent_emote': float('nan'), 'verbosity': float('nan')}
            self.per_text_lists = {'words_per_text': [], 'chars_per_text': [],
                                   'emotes_per_text': []}
            self.occurrence_dicts = {'emotes': dict(), 'words': dict()}
            self.data = pd.DataFrame()

        else:
            # each dict has key name and value thing
            self.count = dict()  # for scalar raw count statistics
            self.prop = dict()  # for statistics that are ratios of two counts
            self.per_text_lists = dict()
            self.occurrence_dicts = dict()
            self.data = data

            # convert the timestamps to a friendly format - this syntax avoids
            # setting a value on a copy of a slice from a dataframe and runs
            # significantly faster
            self.data = self.data.assign(date_sent=self.data['date_sent']
                                                       .astype('datetime64[ns]'))

            # combine all text bodies into a single string
            raw_text = '\n'.join(data['body'].tolist())

            # get cleaned text - create a new column of text body without emotes
            self.data = self.data.assign(
                body_without_emotes=self.data['body'].map(remove_emotes))

            # get text separated into words - create another new column
            self.data = self.data.assign(
                body_words=list(map(get_words, self.data['body_without_emotes'])))

            # get time between texts
            self.data = self.data.assign(
                time_from_last_text=self.data['date_sent'].diff())

            # combine all emote-free text into a single string
            emote_free_text = '\n'.join(self.data['body_without_emotes'].tolist())

            # fill per-text lists
            self.set_per_text_lists()

            # add column of number of words per text
            self.data['words'] = self.per_text_lists['words_per_text']

            # fill dictionary with occurrences of words/emotes
            self.set_occurrence_dicts(raw_text, emote_free_text)

            # fill dictionary of count statistics
            self.set_counts(raw_text, emote_free_text)

            # fill dictionary of proportions
            self.set_props()

    def set_per_text_lists(self):
        """Set the per text list dictionary with words per text, characters per
        text, and emotes per text.
        """
        self.per_text_lists['words_per_text'] = [len(x) for x in
                                                 self.data.body_words]

        self.per_text_lists['chars_per_text'] = self.data['body']\
                                                    .map(len).tolist()

        self.per_text_lists['emotes_per_text'] = self.data['body']\
                                                     .map(count_emotes)\
                                                     .tolist()

    def set_occurrence_dicts(self, raw_text, emote_free_text):
        """Fill a dictionary with the occurrences of each word and each emote.

        Args:
            raw_text (string): the original concatenated text
            emote_free_text (string): the emote/emoji-free concatenated text
        """
        # count emotes/emojis
        self.occurrence_dicts['emotes'] = count_emote_occurrences(raw_text)
        self.occurrence_dicts['words'] = count_word_occurrences(emote_free_text)

    def set_counts(self, raw_text, emote_free_text):
        """Set the count statistics.

        Args:
            raw_text (string): the original concatenated text
            emote_free_text (string): the emote/emoji-free concatenated text
        """
        # count texts
        self.count['texts'] = len(self.data)

        # count words
        self.count['words'] = sum(self.occurrence_dicts['words'].values())

        # count characters
        self.count['chars'] = len(raw_text)
        self.count['spaces'] = sum(c.isspace() for c in raw_text)
        self.count['letters'] = len([c for c in emote_free_text
                                     if c.isalpha()])
        self.count['digits'] = len([c for c in emote_free_text
                                    if c.isdigit()])
        self.count['emotes'] = sum(self.occurrence_dicts['emotes'].values())
        self.count['punct'] = len([c for c in emote_free_text
                                   if c in string.punctuation])

    def set_props(self):
        """Set the proportion statistics."""
        if self.count['texts'] > 0:
            self.prop['words_per_text'] = self.count['words'] / self.count['texts']
        else:
            self.prop['words_per_text'] = float('inf')
        if self.count['punct'] > 0:
            self.prop['laziness'] = self.count['words'] / self.count['punct']
        else:
            self.prop['laziness'] = float('inf')
        if self.count['words'] > 0:
            self.prop['percent_emote'] = (self.count['emotes'] /
                                          self.count['words']) * 100
            self.prop['verbosity'] = self.count['letters'] / self.count['words']
        else:
            self.prop['percent_emote'] = float('nan')
            self.prop['verbosity'] = float('nan')

    def compare_freq(self, other, token):
        """Find differences in word or emoji use frequency.

        Args:
            other (TextSummary): TextSummary to compare to.
            token (string): key of the thing to compare (words or emotes)

        Returns:
            diff_dict (dict): dictionary where keys correspond to words
            and values are tuples (total, expected ratio)

        """
        diff_dict = dict()
        my_dict = self.occurrence_dicts[token]
        other_dict = other.occurrence_dicts[token]
        # get a merged word dictionary
        merged_dict = {**my_dict, **other_dict}

        for word in merged_dict:
            k1 = my_dict[word] if word in my_dict else 0
            k2 = other_dict[word] if word in other_dict else 0
            n1 = self.count[token]
            n2 = other.count[token]
            _, mean, _ = ratio_conf_bounds(k1, n1, k2, n2)
            diff_dict[word] = (k1+k2, mean)
        return diff_dict

    def get_counts(self, word):
        """Find number of occurrences of word in each text.

        Args:
            word (string): the word to find.

        Returns:
            counts (list): list of integer counts.

        """
        return [word_list.count(word) for word_list in
                self.data['body_words']]

    def get_conversations(self, names):
        """Get a list of conversations.

        Args:
            names (list): names of senders.

        Returns:
            convos (list): a list of dictionaries with conversation information

        """
        WINDOW_TIME = pd.Timedelta('30m')  # window in which we count texts
        MIN_WINDOW = 6  # minimum number of texts in window
        MIN_CONVO_TEXTS = 15  # minimum number of texts in a conversation

        # make a copy of the DataFrame that is indexed by date sent
        df_time_indexed = self.data.copy()
        df_time_indexed['int_index'] = self.data.index  # keep the integer indices
        df_time_indexed.index = self.data['date_sent']

        rolling_window = df_time_indexed['words'].rolling(WINDOW_TIME)
        texts_per_window = rolling_window.count()
        convo_active = (texts_per_window >= MIN_WINDOW)  # true inside convo
        convo_boundaries = convo_active.astype('int8').diff()
        # indices of first text in conversation - need to adjust due to window
        convo_starts = df_time_indexed['int_index'][convo_boundaries == 1].values
        convo_starts = [int(ind-texts_per_window[ind]+1) for ind in convo_starts]
        # indices of first text outside of conversation
        convo_ends = df_time_indexed['int_index'][convo_boundaries == -1].values
        if convo_active[0]:  # if initially active, have a convo starting at 0
            convo_starts = np.concatenate(([0], convo_starts))
        # if active at end, have extra convo ending
        if convo_active[len(self.data)-1]:
            convo_ends = np.concatenate((convo_ends, [len(self.data)]))

        # for topic analysis
        r = Rake()

        convos = []
        for ind in range(len(convo_starts)):
            start_ind = convo_starts[ind]
            end_ind = convo_ends[ind]-1  # note: last text *in* convo
            convo_slice = self.data[start_ind:end_ind+1]
            length = len(convo_slice)
            if length < MIN_CONVO_TEXTS:  # too short to count as a conversation
                continue
            start_time = self.data['date_sent'][start_ind]
            end_time = self.data['date_sent'][end_ind]
            duration = end_time - start_time
            convo_slices = [convo_slice[convo_slice['sender'] == sender]
                            for sender in names]
            words = [convo_slice_person['words'].sum() for convo_slice_person in convo_slices]
            total_words = sum(words)

            # find the convo summary
            slice_text = "\n".join(convo_slice['body_without_emotes'])
            r.extract_keywords_from_text(slice_text)
            topic = r.get_ranked_phrases()[0]

            # who started the conversation?
            starter = self.data['sender'][start_ind]
            # who ended it?
            ender = self.data['sender'][end_ind]

            convos.append({'start_ind': start_ind, 'end_ind': end_ind,
                           'start_time': start_time, 'end_time': end_time,
                           'duration': duration, 'length': length,
                           'starter': starter, 'ender': ender,
                           'topic': topic,
                           'words_by_person': dict(zip(names, words)),
                           'total_words': total_words})
        return convos

    def __str__(self):
        return str(self.count)


if __name__ == "__main__":
    START_TIME = time.time()

    df = pd.read_csv(LOADPATH, index_col=False)
    df = convert_raw_csv_types(df)
    ts = TextSummary(df)
    names = list(COLORS.keys())
    convos = ts.get_conversations(names)
    print("Execution time: " + str(time.time() - START_TIME))
