import nextcord
import unicodedata

print(f'Unicode Filter Plugin Loaded')
def normalize_unicode(input_str):
    normalized_str = unicodedata.normalize('NFKD', input_str).encode('ascii', 'ignore').decode('utf-8')
    return normalized_str

def check_bad_words(input_str, bad_words):
    normalized_str = normalize_unicode(input_str)
    return normalized_str in bad_words

async def handle_message(message, bad_words, log_channel_name='logs'):
    if check_bad_words(message.content, bad_words):
        await message.delete()
        await message.channel.send(f"Message '{message.content}' was blocked.")
        log_channel = nextcord.utils.get(message.guild.channels, name=log_channel_name)
        if log_channel:
            await log_channel.send(f"Message '{message.content}' by {message.author} was blocked, Unicode.")
