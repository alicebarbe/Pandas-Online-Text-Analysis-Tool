Config File
===========

The config file (.txt) enables users to easily set paramaters without needing
to really modify the Python code. Be sure to point to it in config.py.

The parameters are described below and are optional unless otherwise specified:

Only specify the chat parsing parameters applicable. At least one of
SIGNAL_SMS_CSV+SIGNAL_MMS_CSV+SIGNAL_RECIPIENT_CSV, WHATSAPP_TXT, GROUPME_JSON,
DISCORD_JSON, or FB_FOLDER must be specified.

For Signal chat parsing:

* *SIGNAL_DB*: location of decrypted Signal .db file. This is used by opendb.py
  to unpack signal messages.
* *SIGNAL_SMS_CSV*: location of Signal sms.csv file (enter after exporting
  using opendb.py).
* *SIGNAL_MMS_CSV*: location of Signal mms.csv file (enter after exporting
  using opendb.py).
* *SIGNAL_RECIPIENT_CSV*: location of Signal recipient.csv file (enter after
  exporting using opendb.py).
* *MY_NAME*: enter your name here, surrounded by quotes. Signal doesn't know
  your name.
* *THREAD*: integer thread number of the relevant Signal chat. This can be
  by looking in for the number in the Thread column of relevant messages in
  the sms/mms csv files.

For other chat parsing:

* *WHATSAPP_TXT*: location of WhatsApp .txt export.
* *WHATSAPP_PSEUDO*: dictionary of the form {"Bob": "Bobby"} where
  "Bobby" is Bob's WhatsApp name. This is necessary if exporting
  across multiple platforms and names/handles need to be matched up.
* *GROUPME_JSON*: location of GroupMe .json export.
* *GROUPME_PSEUDO*: dictionary of the form {"Bob": "Bobby"} where
  "Bobby" is Bob's GroupMe name. This is necessary if exporting
  across multiple platforms and names/handles need to be matched up.
* *DISCORD_JSON*: location of Discord .json export.
* *DISCORD_PSEUDOS*: dictionary of the form {"Bob": "bobthediscordguy"} where
  "bobthediscordguy" is Bob's discord handle. This is necessary if exporting
  across multiple platforms and names/handles need to be matched up.
* *FB_FOLDER*: location of folder containing Facebook Messenger .json exports.
  FB Messenger generally exports a "messages" folder within which there is an
  "inbox" folder within which there are many message folders, one for each
  chat (and two per chat in the case of chats containing multimedia). The
  folder to specify here is of the form messages/inbox/bobsmith_dy28ddkp0.

The PSEUDO dictionaries are optional and will perform a search-replace of the
value (pseudonym) by the key (actual name), so it is only necessary to specify
for users whose names don't match up across platforms.

For main functionality:

* *LOADPATH* (required): this is where the aggregate cleaned chat csv file will
  be stored at the end of running chat_cleaning_aggregate.py, and where the
  plotting programs will fetch data.
* *COLORS*: a dictionary of the form {"Alice": "red", "Bob": "blue"}, where the
  colors are standard matplotlib colors. If not specified, default colors will
  be applied.
* *TOKEN_LIST*: a list of strings to plot the frequency/usage of in
  make_bin_plots and make_heatmap_plots, of the form ["hi", "work"]. Optional.
* *OFFSET* (required for running make_heatmap_plots): the hour of the first
  message sent in the history. *TO-DO: Automate this away*
* *TIMEZONE*: standard string representation of timezone to do the analysis in.
  The default is 'US/Eastern'.

Paramaters unlikely to be useful, but just in case:

* *BIN_FREQ*: default is '1d' for 1 day. This is the size of the binning used
  in make_bin_plots (i.e. the resolution to plot data points). Other useful
  bin sizes could be '1W' for weekly or '1M' for monthly. A list of valid
  options can be found here_.
* *BIN_FREQ_HM*: default is '1h' for 1 hour. This is the bin size for the
  heatmap, i.e. the unit for the x-axis.
* *BIN_FREQ_2*: default is 24. Number of bins of size BIN_FREQ_HM to include in
  one heatmap row.
  
.. _here: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
