import nextcord
import re


print(f'Discord server scam Plugin Loaded')

invite_pattern = re.compile(r"(discord\.gg|discordapp\.com/invite)")
keywords_pattern = re.compile(r"(support|airdrop)")
user_offenses = {}

async def check_message(message):
    # Ignore messages from DMs
    if message.guild is None:
        return

    # Check if the user has any exempt roles
    member = message.guild.get_member(message.author.id)
    exempt_roles = ['mod', 'myst team', 'mysterium wizard', 'pro wizard']
    if any(role.name.lower() in exempt_roles for role in member.roles):
        return

    # Check for both invite links and keywords
    if invite_pattern.search(message.content) and keywords_pattern.search(message.content):
        await message.delete()
        user_id = message.author.id
        if user_id in user_offenses:
            user_offenses[user_id] += 1
        else:
            user_offenses[user_id] = 1

        if user_offenses[user_id] == 1:
            await message.channel.send(f'{message.author.mention}, please refrain from posting support/airdrop messages. You will be banned if you continue.')
        elif user_offenses[user_id] == 2:
            await message.channel.send(f'{message.author.mention} has been banned for repeated offenses.')
            await message.guild.ban(message.author)

def setup(bot):
    bot.add_listener(check_message, "on_message")
