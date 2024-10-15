# Created by Liam Gibbins AKA Epsilonion
# Bot Name: Mysterium - Helper
# Copyright 1997-2024 Tempest Solutions
# This bot has been made for the Mysterium Network Discord Community and shall
# not be copied, distributed or modified without consent of the above.
# This bot is in aid to combat the ever increasing scam's present on discord servers
# and to enhance the server member experience of the community and moderation of the
# community. 

import nextcord
from nextcord.ext import commands
from unicode_filter import handle_message
import http.client
import json
import re
# from Levenshtein import distance as levenshtein_distance # for simular username checking against mod's/admin role members(coming soon)

# Intents specify the events your bot will receive (define the bit)
intents = nextcord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True  
intents.dm_messages = True
intents.guilds = True

# Create an instance of the bot with the specified command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# **** Load plugins ****
import plugin_custom_commands           # Load custom commands plugin
plugin_custom_commands.setup(bot)
import message_purger                   # Load message purger plugin
message_purger.setup(bot)  
import url_filter                       # Load URL filter plugin
url_filter.setup(bot)
import bad_words_filter                 # Load Adult word censorship plugin
bad_words_filter.setup(bot)
import discord_server_url               # Load anti discord link scam plugin
discord_server_url.setup(bot)
import welcome_message                  # Load Welcome message plugin
welcome_message.setup(bot)
import plugin_statistics                # Mysterium Network and node statistics Plugin
plugin_statistics.setup(bot)

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}, READY and ONLINE!')
    
@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run('Your_bot_app_ID')