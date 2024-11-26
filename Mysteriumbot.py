import nextcord
from nextcord.ext import commands, tasks
import mysql.connector
import requests
import os
import logging

# Bot setup
intents = nextcord.Intents.default()
intents.guilds = True
intents.message_content = True
intents.members = True
intents.messages = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Function to load all extensions from the plugins folder
def load_extensions():
    print("Loading extensions...")
    for filename in os.listdir('/app/plugins'):
        if filename.endswith('.py'):
            extension_name = f'plugins.{filename[:-3]}'
            print(f"Loading extension: {extension_name}")
            try:
                bot.load_extension(extension_name)
                print(f"Loaded extension: {extension_name}")
            except Exception as e:
                print(f"Failed to load extension {extension_name}: {e}")



# Load all plugins
load_extensions()

@bot.event
async def on_ready():
    try:
        await bot.sync_all_application_commands()
        print(f'Synced commands for {len(bot.guilds)} guilds.')  # Debug print statement
    except Exception as e:
        print(f'Error syncing commands: {e}')  # Debug print statement
    print(f'Logged in as {bot.user}')
    logging.info(f"Logged in as {bot.user.name} ({bot.user.id})")

@bot.event
async def on_connect():
    print(f'Bot connected to Discord!')


# Run the bot
bot.run('Enter_Bot_TOKEN')

