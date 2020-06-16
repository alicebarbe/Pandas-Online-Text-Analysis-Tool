# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 16:51:53 2019

@author: dgurevich6
"""
import emoji
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'(?<![@#])\b\w+(?:\'\w+)?')
tokenizer_minimal = RegexpTokenizer(r'[a-zA-Z]+')
EMOTES = [':P', ':p', ':)', ':/', ':(', 'XD', ':D']


def isemoji(character):
    """Returns true if the character is an emoji

    Arguments:
        character (str): the character.
    """
    return character in emoji.UNICODE_EMOJI


def strip_subs(text, substring_list):
    """Strip a string of the substrings in a list.
    (Assumption: no substring is contained in another)

    Arguments:
        text (str): input string
        substring_list (list): list of undesired substrings
    Returns:
        clean_text (str): input text with substrings removed.
    """

    clean_text = text
    for subs in substring_list:
        clean_text = clean_text.replace(subs, '')
    return clean_text


def count_word_occurrences(text):
    """Return a dictionary of words and their number of occurrences.

    Arguments:
        clean_text (str): string representation of clean text.

    Returns:
        word_dict (dict): dictionary with entries {word: count}
    """

    word_dict = dict()  # occurrence of each word
    # count by word
    for i in get_words(text.lower()):
        word_dict[i] = word_dict.get(i, 0) + 1
    return word_dict


def get_words(text, minimal=False):
    """Return the words comprising a string.
    Arguments:
        text (string): the original string
        minimal (boolean): if true, break words at ' and -
    Returns:
        word_list (list): a list of words
    """
    # convert to lowercase and split into words
    if minimal:
        word_list = tokenizer_minimal.tokenize(text.lower())
    else:
        word_list = tokenizer.tokenize(text.lower())
    # remove words consisting of only digits
    word_list = [token for token in word_list if not token.isnumeric()]
    return word_list


def count_emote_occurrences(raw_text):
    """Return a dictionary of emoji/emotes and their number of occurrences.

    Arguments:
        raw_text (str): string representation of raw text

    Returns:
        emo_dict (dict): dictionary with entries {emote/emoji: count}
    """

    # emotes/emojis
    emo_dict = dict()  # keeping track of occurrence of each emoji

    # count occurrences of emotes
    for emote in EMOTES:
        emo_dict[emote] = raw_text.count(emote)
    emoji_only = [c for c in raw_text if isemoji(c)]
    # count by emoji
    for i in emoji_only:
        emo_dict[i] = emo_dict.get(i, 0) + 1
    return emo_dict


def remove_emotes(text):
    """Remove emotes from string and return the cleaned string
    Arguments:
        text (string): the original string
    Returns:
        text (string): the string with emotes removed
    """
    for emote in EMOTES:
        text = text.replace(emote, '')
    emoji_only = [c for c in text if isemoji(c)]
    for i in emoji_only:
        text = text.replace(i, '')
    return text


def count_emotes(text):
    """Returns the number of emotes in a string
    Arguments:
        text(string): the original string
    Returns:
        count (int): the number of emotes in the original string
    """
    emote_count = 0
    for emote in EMOTES:
        emote_count += text.count(emote) 
    emote_count += len([c for c in text if isemoji(c)])
    return emote_count
        