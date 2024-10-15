# Helper Discord Bot
This bot is designed to help moderate and combat spam and scams we see on discord everyday.

Modular plugin design to disable features that are not required.

## What does this bot do?
This bot has several main features.

- Regex on Adult word censorship (ignores case of the words) gives "Mute members role" after 5 offences by member for 20 mins applies to single words and phrases.
- Unicode - looks at the adult word list and compares to the Unicode and deletes if necessary.
- URL blocker - strips http/https off URL's and compares to URL text file and deletes message if match found.
- Message Purge for channel - Purges messages of a UsersID  with the !purge <userID> command (Only Admin, mod, mysterium wizard roles).
- Statistics - network statistics and node statistics with !stats and !nodestats <nodeid> commands.
- Support scams - deletes messages with discord server URL and support or airdrop in same message.
- New Member DM - New members recieve a DM with community guidelines and advice on how not to get scammed.

Plugins can be turned on or off if a feature is not required.- New server member DM with welcome, community guidelines and relitive information to your community.

## Still todo
- Username simularity checker logs profiles that have simular usernames of members with simular roles such as admins and moderators to help prevent fake support and associated scam's

## Request a feature
request a feature by adding it to the issue system.

## Install
pip install nextcord python-Levenshtein - for user simularities (not yet included)

### INSTALL Nextcord

Installing¶
You can get the library directly from PyPI:

content_copy
python3 -m pip install -U nextcord
If you are using Windows and have not installed Python to PATH, then the following should be used instead:

content_copy
py -3 -m pip install -U nextcord
To get voice support, you should use nextcord[voice] instead of nextcord, e.g.

content_copy
python3 -m pip install -U nextcord[voice]
On Linux environments, installing voice requires getting the following dependencies:

libffi

libnacl

python3-dev

For a Debian-based system, the following command will get these dependencies:

content_copy
$ apt install libffi-dev libnacl-dev python3-dev
Remember to check your permissions!
