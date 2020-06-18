Config File
===========

The config file (.txt) enables users to easily set paramaters without needing
to really modify the Python code. Be sure to point to it in config.py. If using
relative file locations in config.txt, make them relative to the root
POTATo directory (wherever config.py is), NOT to where config.txt is stored.
This is because the variables will be imported in config.py.

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

* *LOADPATH* (**required**): this is where the aggregate cleaned chat csv file will
  be stored at the end of running chat_cleaning_aggregate.py, and where the
  plotting programs will fetch data.
* *COLORS*: a dictionary of the form {"Alice": "red", "Bob": "blue"}, where the
  colors are standard matplotlib colors. If not specified, default colors will
  be applied.
* *TOKEN_LIST*: a list of strings to plot the frequency/usage of in
  make_bin_plots and make_heatmap_plots, of the form ["hi", "work"]. Optional.
* *TIMEZONE*: standard string representation of timezone to do the analysis in.
  The default is 'US/Eastern'.

Paramaters unlikely to be useful, but just in case:

* *BIN_FREQ*: default is '1d' for 1 day. This is the size of the binning used
  in make_bin_plots (i.e. the resolution to plot data points). Other useful
  bin sizes could be '1W' for weekly or '1M' for monthly. A list of valid
  options can be found here_.
* *BIN_FREQ_HM*: default is '1h' for 1 hour. This is the bin size for the
  heatmap, i.e. the unit for the x-axis.
* *BIN_FREQ2*: default is 24. Number of bins of size BIN_FREQ_HM to include in
  one heatmap row.
* *OFFSET*: default is the hour of the first text. This is used to set the offset
  of the first cell in the heatmaps, in units of BIN_FREQ_HM - change only if
  changing BIN_FREQ_HM and BIN_FREQ2. For example, if you set BIN_FREQ_HM='1d'
  and BIN_FREQ2=7 for a day per cell and a week per row, and you like your
  rows to begin on a Sunday, but the first day you chatted was a Wednesday,
  then set OFFSET to 4.
  
.. _here: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases

Example
-------
In this example, Alice and Bob communicate using Signal, Discord, and Facebook
messenger. Alice's Discord handle is aliceondiscord and Bob's Discord handle is
bobondiscord. Alice is running POTATo.

Alice's file structure is

::

    Pandas-Online-Text-Analysis-Tool
    |
    |___data
    |   |___signal
    |   |   |   signal.db
    |   |   |   ...
    |   |   |   sms.csv
    |   |   |   mms.csv
    |   |   |   recipient.csvDirect Messages - Private - bobondiscord [239102849302938122].json
    |   |   |   ...
    |   |   |
    |   |___bobsmith_30_a8dj37js
    |   |   |   message_1.json
    |   |   |   message_2.json
    |   |   |
    |   |___discord_dms
    |   |   |   Direct Messages - Private - bobondiscord [239102849302938122].json
    |   |   |
    |   |   data.csv
    |   |
    |   config
    |   |   config.txt
    |   |
    |   chat_cleaning_aggregate.py
    |   config.py
    |   ...

Note that the relative file paths are relative to the root directory, not the
config folder.

::

    # For signal parsing
    MY_NAME : "Alice"  # name of signal owner
    THREAD : 8  # signal THREAD number
    
    # data files
    SIGNAL_DB : 'data/signal/signal.db'
    SIGNAL_SMS_CSV : 'data/signal/sms.csv'
    SIGNAL_MMS_CSV : 'data/signal/mms.csv'
    SIGNAL_RECIPIENT_CSV : 'data/signal/recipient.csv'
    DISCORD_JSON : 'data/discord_dms/Direct Messages - Private - bobondiscord [239102849302938122].json'
    DISCORD_PSEUDOS : {'Alice': 'aliceondiscord', 'Bob': 'bobondiscord'}
    FB_FOLDER: "data/bobsmith_30_a8dj37js"
    
    LOADPATH : 'data/data.csv'
    
    # plot settings
    COLORS : {'Alice': 'red', 'Bob': 'blue'}
    
    # list of words/emotes to search
    TOKEN_LIST : ['hi', 'work', 'funny', ':)']
    
If Alice wants to make a heatmap with days as cells and weeks as rows, add:

::

    BIN_FREQ_HM: '1d'
    BIN_FREQ2: 7
    OFFSET: 3
    
