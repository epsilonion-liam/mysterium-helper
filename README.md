# Helper Discord Bot
This bot is designed to help moderate and combat spam and scams we see on discord everyday.

## What does this bot do?
This bot has several main features.

- Adult and bad word cesorship with Redex (builds patterns to recognise upper and lowercase ways of spelling a bad word), able to expand list of words to recognise.
- Disorc invite server URL spupport scams and spam in messages and DM's- Matches a pattern for discord server URL's and keywords in the same message, deletes the message and warns the user then bans them if they persist, able to expand keywords but allows specific roles to send invites such as mods and admins.
- New server member DM with welcome, community guidelines and relitive information to your community.
- Username simularity checker logs profiles that have simular usernames of members with simular roles such as admins and moderators to help prevent fake support and associated scam's

## Request a feature
request a feature by adding it to the issue system.

## Install
pip install nextcord python-Levenshtein

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