Exporting Chats
===============

It is recommended to place chat export files in a folder called "data", placed
in the root POTATo directory. This is not strictly necessary - the config file
can point to files in any location - but it makes life easier.

Facebook Messenger
------------------

To export Facebook Messenger chats:

1. Log into Facebook. In the upper right hand corner, find *Settings&Privacy > Settings*.
2. In the *Your Facebook Information* tab, click *Download Your Information*.
3. Change Format option to JSON and set Media Quality to Low for a faster download.
   Click Deselect All and select only the *Messages* box.
4. Click *Create File* and wait. You will get a notification when the export
   is finished - this may take several hours. It will be available under
   *Available Copies* for a few days. Click *Download* and extract the contents
   of the resulting zipped folder.
5. The contents are a *messages* folder. Open it and open the *inbox* folder in it.
   The folders in *inbox* each correspond to a chat. In chats with multimedia
   content, there are two folders - one named in camel case and one named with only
   lowercase letters. The camel case folder contains media, the lowercase letter
   folder contains the message json folders.
6. Copy the lowercase letter folder (bobsmith_3_s2ekwl39s0) to a data folder in
   the root POTATo directory.
   Be mindful to copy the folder, not just its contents (*message_1.json, etc.*).

::
    
    messages
    |___inbox
    |   |___bobsmith_3_s2ekwl39s0  <-- COPY THIS FOLDER
    |   |   |   message_1.json
    |   |   |   message_2.json
    |   |___BobSmith_3_S2eKWl39s0
    |   |   |___files
    |   |   |___gifs
    |   |   |___photos
    |   |   |___videos
    |___message_requests
    |___stickers_used


GroupMe
-------

To export GroupMe chats:

1. Log into GroupMe at groupme.com. Click on your profile picture on the upper
   left hand corner. Click on *Export My Data*. 
2. Click on *Create Export*. Select *Message Data* and click *Next*.
3. Select the relevant chats to export and click *Next*. Wait for the email
   notification. The Export will be avaiable to download for a day in the
   *Export My Data* page - download it and extract the contents of the
   resulting zipped folder.
4. There will be one folder per chat. The *message.json* file in each chat folder
   is the chat message export for that chat. Copy it and place it in a data
   folder in the root POTATo directory.

::

    392830401
    |___likes
    |   |   everyone.json
    |   |   for_me.json
    |   |   mine.json
    |   conversation.json
    |   message.json  <-- COPY THIS FILE

   
WhatsApp
--------

To export a WhatsApp chat:

1. Open the WhatsApp app on your phone. Open a relevant chat and click on the
   three dots in upper right hand corner, select *More*, select *Export chat*.
2. If prompted, select *Without media* to speed up the process. Select a
   convenient way to transfer it to your computer (emailing or whatsapping it 
   to yourself, for example).
3. Save the resulting .txt file in a data folder in the root POTATo directory.

Discord
-------

Discord currently does not support directly exporting chats.
The easiest way to do it seems to be through Alexey Golub's (@Tyrrz) amazing
library, DiscordChatExporter: https://github.com/Tyrrrz/DiscordChatExporter

The procedure is fairly simple and very well documented in his wiki.
If using the GUI, select JSON as export format and "yyyy-MM-dd HH:mm:ss tt"
as the time format.
If using the CLI, add the following options:

::
    
    -f Json --dateformat "yyyy-MM-dd HH:mm:ss tt"
    
Signal
------

The procedure for exporting Signal chats is somewhat complicated, due to the
fact that Signal does not provide a built-in way to export chats or decrypt
their backups. We have found that this is the simplest way to do it:

Getting the backup:

1. Follow the instructions here to create a Signal backup: https://support.signal.org/hc/en-us/articles/360007059752-Backup-and-Restore-Messages
2. Remember to save the passcode! It will be necessary to decrypt the backup.
3. Find the backup in your phone file system (generally in a Signal/Backup folder) and transfer it to your computer.

Decrypting the backup:

There are multiple Signal backup decrypting libraries on Github, but of all the ones we've tried, Tim van der Molen's Sigbak is by far the easiest and fastest: 
https://www.kariliq.nl/sigbak/ (also available on Github: https://github.com/tbvdm/sigbak). His documentation is excellent and we recommend that you check it out. For the purposes of POTATo, the following command is sufficient once installation is complete (which should be as simple as just running :code:`make` and then :code:`make install` in the repository after downloading/cloning it):

::

    sigback sqlite mysignal.backup signal.db

Easily find your thread ID numbers (an identifier for each conversation) by typing:

::

    sigbak threads mysignal.backup
    
The :code:`-p my_passcode.txt` flag can be quite useful in both cases, where the my_passcode.txt is the 15-digit decryption passcode.

The resulting signal.db file is used in chat_cleaning/opendb.py which unpacks tables inside into csv files, among which are recipient.csv, sms.csv, and mms.csv.
