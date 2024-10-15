import nextcord
import unicodedata
import re

print(f'Unicode Filter Plugin Loaded')

def normalize_unicode(input_str):
    normalized_str = unicodedata.normalize('NFKD', input_str).encode('ascii', 'ignore').decode('utf-8')
    return normalized_str

def check_bad_words(input_str, bad_words):
    normalized_str = normalize_unicode(input_str)
    return normalized_str in bad_words

def check_bad_phrases(input_str, bad_phrases):
    normalized_str = normalize_unicode(input_str)
    for phrase in bad_phrases:
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        if pattern.search(normalized_str):
            return True
    return False

async def handle_message(message, bad_words, bad_phrases, log_channel_name='logs'):
    if check_bad_words(message.content, bad_words) or check_bad_phrases(message.content, bad_phrases):
        await message.delete()
        await message.channel.send(f"Message '{message.content}' was blocked.")
        log_channel = nextcord.utils.get(message.guild.channels, name=log_channel_name)
        if log_channel:
            await log_channel.send(f"Message '{message.content}' by {message.author} was blocked, Unicode.")

def load_bad_words(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Load bad words and phrases from bad_word.txt
bad_words = load_bad_words('bad_words.txt')
bad_phrases = load_bad_words('bad_words.txt')
