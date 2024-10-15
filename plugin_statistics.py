import nextcord
import http.client
import json
from nextcord.ext import commands

# Intents specify the events your bot will receive (define the bit)
intents = nextcord.Intents.default()
intents.message_content = True

# Create an instance of the bot with the specified command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

print(f'Network and node statistics Plugin Loaded')

# Command to show overall statistics
#def setup(bot):
    

def fetch_data(host, endpoint):
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", endpoint)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    conn.close()
    return json.loads(data)

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
        
        print(f'Returned stats from API')
        return (total_ids, ids_per_country, average_quality, average_latency, average_uptime, average_bandwidth, total_residential, total_hosting)
    
    else:
        raise ValueError("Unexpected error, API Issues")

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

def setup(bot):
    @bot.command()
    async def proposals(ctx):
        stats = fetch_proposals_statistics()
        await ctx.send(f"Total Proposals: {stats[0]}, Quality: {stats[2]:.2f}, Latency: {stats[3]:.2f}ms")

    @bot.command()
    async def node(ctx, node_id):
        try:
            node_stats = fetch_node_stats(node_id)
            await ctx.send(f"Node ID: {node_id}, Quality: {node_stats[0]:.2f}, Latency: {node_stats[1]:.2f}ms, Uptime: {node_stats[2]:.2f}, Bandwidth: {node_stats[3]:.2f}MB, IP Type: {node_stats[4]}, Country: {node_stats[5]}, City: {node_stats[6]}, ISP: {node_stats[7]}")
        except ValueError as e:
            await ctx.send(str(e))
            
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
