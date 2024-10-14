import nextcord
from nextcord.ext import commands
import http.client
import json
import re
import message_purger

# Intents specify the events your bot will receive (define the bot)
intents = nextcord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.dm_messages = True
intents.guilds = True

# Create an instance of the bot with the specified command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}, READY!')

# keep track of warnings for each user
user_offenses = {}

# Read bad words from file
with open('bad_words.txt', 'r') as file:
    bad_words = [line.strip() for line in file]
    print(f'Loaded Bad and Adult word file')

# Create regex pattern for bad words
bad_words_pattern = re.compile('|'.join(bad_words), re.IGNORECASE)
invite_pattern = re.compile(r'(https?:\/\/)?(www\.)?(discord\.(gg|io|me|li|com)\/[a-zA-Z0-9]+)', re.IGNORECASE)
keywords_pattern = re.compile(r'\b(support|airdrop)\b', re.IGNORECASE)
print(f'Created Regex patterns from words in bad and adult word file')

# **** API STATISTICS ****

# Function to fetch data from a given API endpoint
def fetch_data(host, endpoint):
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", endpoint)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    conn.close()
    return json.loads(data)

# Function to fetch and calculate proposals statistics
def fetch_proposals_statistics():
    data = fetch_data('discovery.mysterium.network', '/api/v4/proposals?&access_policy=all')
    
    if isinstance(data, list):
        proposals = data

        total_ids = len(proposals)
        ids_per_country = {}
        total_quality = total_latency = total_uptime = total_bandwidth = 0
        total_residential = total_hosting = 0

        for proposal in proposals:
            country = proposal['location']['country']
            ids_per_country[country] = ids_per_country.get(country, 0) + 1

            total_quality += proposal['quality']['quality']
            total_latency += proposal['quality']['latency']
            total_uptime += proposal['quality']['uptime']
            total_bandwidth += proposal['quality']['bandwidth']

            ip_type = proposal['location']['ip_type']
            if ip_type == 'residential':
                total_residential += 1
            else:
                total_hosting += 1

        average_quality = total_quality / total_ids if total_ids > 0 else 0
        average_latency = total_latency / total_ids if total_ids > 0 else 0
        average_uptime = total_uptime / total_ids if total_ids > 0 else 0
        average_bandwidth = total_bandwidth / total_ids if total_ids > 0 else 0

        return (total_ids, ids_per_country, average_quality, average_latency, 
                average_uptime, average_bandwidth, total_residential, total_hosting)
        print(f'Returned stats from API')
    else:
        raise ValueError("Unexpected JSON structure")

# Function to fetch node statistics for a specific node ID
def fetch_node_stats(node_id):
    endpoint = f'/api/v3/proposals?&access_policy=all&provider_id={node_id}'
    data = fetch_data('discovery.mysterium.network', endpoint)
    
    if isinstance(data, list):
        proposals = data

        if len(proposals) > 0:
            node_stats = proposals[0]  # Assuming we want the first proposal for this node
            quality = node_stats['quality']['quality']
            latency = node_stats['quality']['latency']
            uptime = node_stats['quality']['uptime']
            bandwidth = node_stats['quality']['bandwidth']
            ip_type = node_stats['location']['ip_type']
            country = node_stats['location']['country']
            city = node_stats['location']['city']
            isp = node_stats['location']['isp']
            return (quality, latency, uptime, bandwidth, ip_type, country, city, isp)
        else:
            raise ValueError("No proposals found for this node, possibly the node is offline.")
    else:
        raise ValueError("Node is OFFLINE!")

# Event listener for new member join events
@bot.event
async def on_member_join(member):
    guild = member.guild
    existing_members = guild.members
    report_channel_id = 1242733447387283486  # Report channel ID
    report_channel = bot.get_channel(report_channel_id)
   
    # *** Setup new member DM for user giudlines in our community etc

    embed = nextcord.Embed(title="Welcome to the Mysterium Discord!", color=0x00ff00)
   # embed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing
    embed.add_field(name="", value="The Mysterium Discord support team will never ask for your wallet private key.", inline=False)
    embed.add_field(name="", value="The Mysterium Discord support team will never DM. If you get a message saying support, its probably not the official mysterium support team.", inline=False)
    embed.add_field(name="", value="The Mysterium support team will never ask for any personal data from you.", inline=False)
    embed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing
    embed.add_field(name="", value="Scams are becoming a big problem on Discord servers. We are trying to limit the impact that experience whilst within our community.", inline=False)
    embed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing
    embed.add_field(name="", value="Please be considerate and respectful with our community.", inline=False)
    #embed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing
    embed.add_field(name="", value="Help is given by Mysterium Wizards that are not paid to give support and are a members of the community like you.", inline=False)
    embed.add_field(name="", value="If you have an urgent issue that needs to be elevated to the official support the wizards or admin/moderators can elivate your issue for you or provide an email address where you can gain support.", inline=False)
    
    try:
        await member.send(embed=embed)
        print(f"Intro DM sent to new User {member.name}")
    except Exception as e:
        print(f'Could not send DM to {member.name}: {e}')
        print(f"New USER DM: {member.name} has DM turned off")

# Command to show overall statistics
@bot.command(name='stats')
async def stats(ctx):
    try:
        (total_ids, ids_per_country, average_quality, average_latency, 
        average_uptime, average_bandwidth, total_residential, total_hosting) = fetch_proposals_statistics()

        stats_embed = nextcord.Embed(title="Mysterium Network Statistics", color=0x00ff00)
        stats_embed.add_field(name="Total Nodes", value=total_ids, inline=False)
        #stats_embed.add_field(name="IDs per country", value=ids_per_country, inline=False)  # Optional
        stats_embed.add_field(name="Average Quality", value=f"{average_quality:.2f}", inline=True)
        stats_embed.add_field(name="Average Latency", value=f"{average_latency:.2f} ms", inline=True)
        stats_embed.add_field(name="Average Uptime", value=f"{average_uptime:.2f} hours", inline=True)
        stats_embed.add_field(name="Average Bandwidth", value=f"{average_bandwidth:.2f} Mbps", inline=True)
        stats_embed.add_field(name="Total Residential IPs", value=total_residential, inline=True)
        stats_embed.add_field(name="Total Hosting IPs", value=total_hosting, inline=True)
        stats_embed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing

        await ctx.send(embed=stats_embed)
    except Exception as e:
    
        await ctx.send(f"Error: {e}")

# Command to show node statistics
@bot.command(name='nodestats')
async def nodestats(ctx, node_id: str):
    try:
        quality, latency, uptime, bandwidth, ip_type, country, city, isp = fetch_node_stats(node_id)

        node_stats_embed = nextcord.Embed(title="Your Node Statistics", color=0x00ff00)
        node_stats_embed.add_field(name="Quality", value=f"{quality:.2f}", inline=True)
        node_stats_embed.add_field(name="Latency", value=f"{latency:.2f} ms", inline=True)
        node_stats_embed.add_field(name="Uptime", value=f"{uptime:.2f} hours", inline=True)
        node_stats_embed.add_field(name="Bandwidth", value=f"{bandwidth:.2f} Mbps", inline=True)
        node_stats_embed.add_field(name="IP Type", value=ip_type, inline=True)
        node_stats_embed.add_field(name="Country", value=country, inline=True)
        node_stats_embed.add_field(name="City", value=city, inline=True)
        node_stats_embed.add_field(name="ISP", value=isp, inline=True)

        await ctx.send(embed=node_stats_embed)
    except Exception as e:
        await ctx.send(f"Error: {e}")
    
    # Custom commands for answering questions
@bot.command(name="rundocker")
async def rundocker(ctx):
    await ctx.send('Follow this guide to install your node on Docker\nhttps://help.mystnodes.com/en/articles/8006242-how-to-spin-up-a-node-on-docker')

@bot.command(name="runlinux")
async def runlinux(ctx):
    await ctx.send('Follow this guide to install your node on native Linux\nhttps://help.mystnodes.com/en/articles/8006183-linux-guide')

@bot.command(name="backupid")
async def backupid(ctx):
    await ctx.send('Follow this link to find out how to backup or migrate your nodes\nhttps://help.mystnodes.com/en/articles/8005511-migrating-your-node')

@bot.command(name="stakingmyst")
async def stakingmyst(ctx):
    await ctx.send('It is easy to stake and withdraw your stake follow these simple staps:\n 1. Go to https://app.iq.space/\n2. Connect your MetaMask wallet\n3. Deposit MYST token\nYou will need a small amount of POL (was Matic) for gas fees.\n\n If you get an error about your limits visit https://revoke.cash/ connect your wallet anlet and set a new limit if needed')

@bot.command(name="nodesafety")
async def nodesafety(ctx):
    await ctx.send('Follow the link below to read on running an exit node and how to protect yourself\n https://help.mystnodes.com/en/articles/8005105-can-my-node-be-used-for-illegal-activities-how-do-we-protect-node-runners\n https://dvpnalliance.org/exit-node/\nAny further questions can be asked at help@mysterium.network')

@bot.command(name="mystopennat")
async def mystopennat(ctx):
    await ctx.send('You can achieve open NAT by manually forwarding ports as described in the article linked\nhttps://help.mystnodes.com/en/articles/8005269-manual-port-forwarding')

@bot.command(name="nodequality")

async def nodequality(ctx):
    await ctx.send('Enter this URL in your browser and replace nodeID with your nodes ID https://discovery.mysterium.network/api/v3/proposals?&access_policy=all&provider_id=<your_nodes_ID_Here>')

@bot.command(name="help")
async def help_command(ctx):
    helpembed = nextcord.Embed(title="Mysterium Helper v0.9.1", description="Written by Liam Gibbins AKA epsilonion, this bot has been created and will be updated with new features as requests from the community come in.\n The bot is aimed to combat spam and help the community with any issue that they may need help for. \n I would like to thank Adine for his work on the API endpoints that have been adapted for use on the bot. \n\n Road map -\n * To display current token price with daily shift to be added to the !stats command \n * Add more stats to the !stats custom command such as current Fee etc \n * Read file lists for blocked URLs",color=0x00ff00)
    helpembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1293610332090007553/1293610365380198483/00002-3113208706.png?ex=67080009&is=6706ae89&hm=eb77b4a04fa5060da0a921b4699f025ce65ce701700cba1886f7fc87d910b668&")
    helpembed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing
    helpembed.add_field(name="Features of this bot", value="* Sends a DM to new server members with important information about DM support scams and community guidelines. \n * Removes spam invites for support and bans after 3 warnings except admin, mod, mysterium wizard and pro wizard roles. \n * Custom commands for supplying easy support for frequent questions. \n * Adult word censoring. \n * Displays Node Quality stats with the !nodestats <nodeID> custom command \n * Display Networks statsistics with the !stats custom command", inline=False)
    helpembed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing

    helpembed.add_field(name="", value="Custom Commands", inline=False)
    helpembed.add_field(name="!nodestats", value="!node <API Key> displays node quality stats", inline=False)
    helpembed.add_field(name="!stats", value="Dislays Network stats", inline=False)
    helpembed.add_field(name="!rundocker", value="Displays a link to my.mystnodes help page", inline=False)
    helpembed.add_field(name="!runlinux", value="Displays a link to my.mystnodes help page", inline=False)
    helpembed.add_field(name="!backupid", value="Displays a link to my.mystnodes help page", inline=False)
    helpembed.add_field(name="!stakingmyst", value="Displays a link to my.mystnodes help page", inline=False)
    helpembed.add_field(name="!nodesafety", value="Displays a link to my.mystnodes help page", inline=False)
    helpembed.add_field(name="!mystopennat", value="Displays a link to my.mystnodes help page", inline=False) 
    helpembed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing
    await ctx.send(embed=helpembed)

@bot.event
async def check_message(message):       # **** Check Messages for adult cesnsorship and scam support URL messages **>
    # Ignore messages from DMs
    if message.guild is None:
        return

    # Check if the user has any exempt roles
    member = message.guild.get_member(message.author.id)
    exempt_roles = ['admin', 'mod', 'myst team', 'mysterium wizard', 'pro wizard']
    if any(role.name.lower() in exempt_roles for role in member.roles):
        return

    # Check for bad words
    if bad_words_pattern.search(message.content):
        await message.delete()
        user_id = message.author.id

        if user_id in user_offenses:
            user_offenses[user_id] += 1
        else:
            user_offenses[user_id] = 1

        if user_offenses[user_id] == 1:
            await message.channel.send(f'{message.author.mention}, please refrain from using inappropriate language, this community if family friendly.  You will be banned if you continue!.')
        elif user_offenses[user_id] == 3:
            await message.channel.send(f'{message.author.mention} has been banned for repeated use of inappropriate language.')
            await message.guild.ban(message.author)

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

@bot.event
async def on_message(message):
    await check_message(message)
    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    await check_message(after)

# Load message purger plugin
message_purger.setup(bot)

bot.run('your_BOT_code')
