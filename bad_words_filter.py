import nextcord
import re
import asyncio

def load_bad_words():
    with open('bad_words.txt', 'r') as file:
        return [line.strip() for line in file]

bad_words = load_bad_words()

# Create regex pattern for bad words, ignoring case
bad_words_pattern = re.compile('|'.join(re.escape(word) for word in bad_words), re.IGNORECASE)

# Track user offenses
user_offenses = {}

async def handle_bad_words(message):
    # Ignore messages from the bot itself
    if message.author.bot:
        return

    # Check for bad words
    if bad_words_pattern.search(message.content):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, this is a family-friendly community. Please don't post offensive words.")
        
        user_id = message.author.id
        if user_id in user_offenses:
            user_offenses[user_id] += 1
        else:
            user_offenses[user_id] = 1
        
        if user_offenses[user_id] >= 5:
            # Mute the user for 20 minutes
            muted_role = nextcord.utils.get(message.guild.roles, name='Muted Members')
            if muted_role:
                await message.author.add_roles(muted_role)
                await message.channel.send(f"{message.author.mention} has been muted for 20 minutes due to repeated offenses.")
                
                await asyncio.sleep(1200)  # 1200 seconds = 20 minutes
                await message.author.remove_roles(muted_role)
                await message.channel.send(f"{message.author.mention} has been unmuted.")

def setup(bot):
    bot.add_listener(handle_bad_words, "on_message")
