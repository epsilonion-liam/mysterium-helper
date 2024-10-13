# install this -> pip install nextcord python-Levenshtein


import nextcord
from nextcord.ext import commands
from Levenshtein import distance as levenshtein_distance

# Define the bot
intents = nextcord.Intents.default()
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

def find_similar_usernames(new_member, existing_members, threshold=3):
    similar_usernames = []
    for member in existing_members:
        if any(role.name.lower() in ['mod', 'admin', 'myst team', 'mysterium wizard', 'pro wizard'] for role in member.roles):
            if levenshtein_distance(new_member.name, member.name) < threshold:
                similar_usernames.append(member.name)
    return similar_usernames

@bot.event
async def on_member_join(member):
    guild = member.guild
    existing_members = guild.members
    report_channel_id = 1242733447387283486  # Report channel ID
    report_channel = bot.get_channel(report_channel_id)
    
    # Check for similar usernames
    similar_usernames = find_similar_usernames(member, existing_members)
    if similar_usernames:
        await report_channel.send(f"@mod @admin Username similarities detected with {member.mention}")


bot.run('YMTI5MzQ5Nzk3NjExOTA5OTQwMg.GiSK8K.T-1HCNjYq1gEmWZ9MEKHCHJhZHfobwZDuz0mHM')
