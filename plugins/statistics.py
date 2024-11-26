import nextcord
from nextcord.ext import commands
import http.client
import json

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
        
        return (total_ids, ids_per_country, average_quality, average_latency, average_uptime, average_bandwidth, total_residential, total_hosting)
    else:
        raise ValueError("Unexpected error, API Issues")

def fetch_node_stats(node_id):
    endpoint = f'/api/v4/proposals?&access_policy=all&provider_id={node_id}'
    data = fetch_data('discovery.mysterium.network', endpoint)
    if isinstance(data, list):
        proposals = data
        if len(proposals) > 0:
            node_stats = proposals[0]
            quality = node_stats['quality']['quality']
            latency = node_stats['quality']['latency']
            uptime = node_stats['quality']['uptime']
            bandwidth = node_stats['quality']['bandwidth']
            packetLoss = node_stats['quality']['packetLoss']
            ip_type = node_stats['location']['ip_type']
            country = node_stats['location']['country']
            city = node_stats['location']['city']
            isp = node_stats['location']['isp']
            return (quality, latency, uptime, bandwidth, packetLoss, ip_type, country, city, isp)
        else:
            raise ValueError("No proposals found for this node, possibly the node is offline.")
    else:
        raise ValueError("Node is OFFLINE!")

class MysteriumNetworkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Show overall Mysterium network statistics")
    async def proposals(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        stats = fetch_proposals_statistics()
        await interaction.followup.send(f"Total Proposals: {stats[0]}, Quality: {stats[2]:.2f}, Latency: {stats[3]:.2f}ms")

    @nextcord.slash_command(name='stats', description="Show detailed Mysterium network statistics")
    async def stats(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        try:
            (total_ids, ids_per_country, average_quality, average_latency, 
            average_uptime, average_bandwidth, total_residential, total_hosting) = fetch_proposals_statistics()

            stats_embed = nextcord.Embed(title="Mysterium Network Statistics", color=0x00ff00)
            stats_embed.add_field(name="Total Nodes", value=total_ids, inline=False)
            stats_embed.add_field(name="Average Quality", value=f"{average_quality:.2f}", inline=True)
            stats_embed.add_field(name="Average Latency", value=f"{average_latency:.2f} ms", inline=True)
            stats_embed.add_field(name="Average Uptime", value=f"{average_uptime:.2f} hours", inline=True)
            stats_embed.add_field(name="Average Bandwidth", value=f"{average_bandwidth:.2f} Mbps", inline=True)
            stats_embed.add_field(name="Total Residential IPs", value=total_residential, inline=True)
            stats_embed.add_field(name="Total Hosting IPs", value=total_hosting, inline=True)

            await interaction.followup.send(embed=stats_embed)
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")

    @nextcord.slash_command(name='nodestats', description="Show detailed statistics for a specific node")
    async def nodestats(self, interaction: nextcord.Interaction, node_id: str):
        await interaction.response.defer()
        try:
            quality, latency, uptime, bandwidth, packetLoss, ip_type, country, city, isp = fetch_node_stats(node_id)

            node_stats_embed = nextcord.Embed(title="Your Node Statistics", color=0x00ff00)
            node_stats_embed.add_field(name="Quality", value=f"{quality:.2f}", inline=True)
            node_stats_embed.add_field(name="Latency", value=f"{latency:.2f} ms", inline=True)
            node_stats_embed.add_field(name="Uptime", value=f"{uptime:.2f} hours", inline=True)
            node_stats_embed.add_field(name="Bandwidth", value=f"{bandwidth:.2f} Mbps", inline=True)
            node_stats_embed.add_field(name="Packet Loss", value=f"{packetLoss:.2f} %", inline=True)
            node_stats_embed.add_field(name="IP Type", value=ip_type, inline=True)
            node_stats_embed.add_field(name="Country", value=country, inline=True)
            node_stats_embed.add_field(name="City", value=city, inline=True)
            node_stats_embed.add_field(name="ISP", value=isp, inline=True)

            await interaction.followup.send(embed=node_stats_embed)
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")

def setup(bot):
    try:
        bot.add_cog(MysteriumNetworkCog(bot))
        print("StatisticsCog loaded successfully.")
    except Exception as e:
        print(f"Failed to load StatisticsCog: {e}")
