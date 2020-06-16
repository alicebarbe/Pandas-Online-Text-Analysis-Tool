# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:07:30 2019

@author: ABarbe
Found on: https://stackoverflow.com/questions/305378/list-of-tables-db-schema-dump-etc-using-the-python-sqlite3-api
"""

import sqlite3
import pandas as pd
import yaml


def to_csv(filepath):
    """Converts a .db sqlite file to csv files for each database
    Arguments:
        filepath (str): filepath of the database file.
    """
    db = sqlite3.connect(filepath)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * from %s" % table_name, db)
        table.to_csv(table_name + '.csv', index_label='index')
    cursor.close()
    db.close()


if __name__ == '__main__':
    # open configuration file and load its variables globally
    with open('../config.txt', 'r') as configfile:
        config = configfile.read()
    config_dict = yaml.safe_load(config)
    globals().update(config_dict)
    to_csv("../" + SIGNAL_DB)
