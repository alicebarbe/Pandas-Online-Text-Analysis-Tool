Chat Format
===========

For the analysis to work, the chat data must be converted to a uniform
format. This is the hardest part to automate for everyone, since each
chat platform exports in a different raw format. Ultimately, though, the
goal is to create a table stored as a csv file with the following
format:

+-----------------------+----------+--------+-----------------------+
| date_sent             | platform | sender | body                  |
+=======================+==========+========+=======================+
| 2019-11-17            | whatsapp | Alice  | Are you going to the  |
| 09:20:00.000000       |          |        | meeting today?        |
+-----------------------+----------+--------+-----------------------+
| 2019-11-17            | whatsapp | Bob    | Yes I will be         |
| 09:30:00.000000       |          |        |                       |
+-----------------------+----------+--------+-----------------------+
| 2019-11-17            | whatsapp | Alice  | Awesome, see you then |
| 09:31:00.000000       |          |        |                       |
+-----------------------+----------+--------+-----------------------+

If we wanted to add further functionality by considering additional
data, like if the message contains an attachment (an image or a gif, for
example), or when the message was read, or if the message was quoting
another message, then those would need to additional columns in the data
structure. As it is, we’ve chosen to stick to these date sent, platform,
sender, and body, because this information can be obtained from all chat
platform exports.

The processes for how to convert an export into this format varies from
platform to platform and is described below.

JSON exports (FB Messenger, Groupme, Discord)
---------------------------------------------

It’s most common for chat apps to export histories to JSON files: in
this category, we’ve written chat parsers for Facebook Messenger,
GroupMe, and Discord. The table below describes the relevant JSON tags
and some extra information.

+-------------+-------------+-------------+-------------+-------------+
| Platform    | date_sent   | sender      | body        | note        |
+=============+=============+=============+=============+=============+
| Facebook    | t           | sender_name | content     | Exports     |
| Messenger   | imestamp_ms |             |             | chat        |
|             |             |             |             | histories   |
|             |             |             |             | to folders  |
|             |             |             |             | with JSON   |
|             |             |             |             | files -     |
|             |             |             |             | each        |
|             |             |             |             | contains a  |
|             |             |             |             | maximum of  |
|             |             |             |             | 10k         |
|             |             |             |             | messages in |
|             |             |             |             | reverse     |
|             |             |             |             | ch          |
|             |             |             |             | ronological |
|             |             |             |             | order, a    |
|             |             |             |             | folder per  |
|             |             |             |             | chat. Names |
|             |             |             |             | are the     |
|             |             |             |             | user’s      |
|             |             |             |             | facebook    |
|             |             |             |             | profile     |
|             |             |             |             | name.       |
+-------------+-------------+-------------+-------------+-------------+
| GroupMe     | created_at  | name        | text        | Names are   |
|             |             |             |             | the user’s  |
|             |             |             |             | GroupMe     |
|             |             |             |             | profile     |
|             |             |             |             | name        |
+-------------+-------------+-------------+-------------+-------------+
| Discord     | timestamp   | author      | content     | Names are   |
|             |             |             |             | the user’s  |
|             |             |             |             | Discord     |
|             |             |             |             | handle (not |
|             |             |             |             | including   |
|             |             |             |             | #XXXX)      |
+-------------+-------------+-------------+-------------+-------------+

WhatsApp
--------

Whatsapp exports chats up to 40k messages in plaintext in the following
format:

::

   11/17/19, 09:20 - Alice Doe: Are you going to the meeting today?
   11/17/19, 09:30 - Bob Smith: Yes I will be
   11/17/19, 09:31 - Alice Doe: Awesome, see you then

The time is converted to the timezone of the user at time of export. The
messages are parsed along the ‘-’ and ‘:’ symbols. Note that WhatsApp
exports are accurate within a minute (contrary to other platforms, which
generally provide second to millisecond accuracy).

Creating the export without media attachments (recommended) will replace
messages consisting purely of an attachment with “”. This phrase is
converted to a blank space in the parser.

Signal
------