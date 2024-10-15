import nextcord

print(f'URL Blacklist Plugin Loaded')

def load_url_list(filepath):
    with open(filepath, 'r') as file:
        url_list = [line.strip().replace('http://', '').replace('https://', '') for line in file.readlines()]
    return url_list

def contains_blocked_url(message, url_list):
    message_content = message.content.replace('http://', '').replace('https://', '')
    return any(url in message_content for url in url_list)

async def handle_url_message(message, url_list, log_channel_name='logs'):
    # Don't let the bot reply to itself
    if message.author.bot:
        return

    if contains_blocked_url(message, url_list):
        await message.delete()
        await message.channel.send(f"Message was blocked because it contains a blocked URL.")
        log_channel = nextcord.utils.get(message.guild.channels, name=log_channel_name)
        if log_channel:
            await log_channel.send(f"Message '{message.content}' by {message.author} was blocked because it contained a blocked URL.")

def setup(bot):
    bot.load_url_list = load_url_list
    bot.handle_url_message = handle_url_message
