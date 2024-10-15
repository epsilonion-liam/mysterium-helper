import nextcord

async def on_member_join(member):
    guild = member.guild
    report_channel_id = 1295311064313102366  # Report channel ID
    report_channel = member.guild.get_channel(report_channel_id)

    # Setup new member DM for user guidelines in our community etc
    embed = nextcord.Embed(title="Welcome to the Mysterium Discord!", color=0x00ff00)
    embed.add_field(name="", value="The Mysterium Discord support team will never ask for your wallet private key.", inline=False)
    embed.add_field(name="", value="The Mysterium Discord support team will never DM. If you get a message saying support, it's probably not the official Mysterium support team.", inline=False)
    embed.add_field(name="", value="The Mysterium support team will never ask for any personal data from you.", inline=False)
    embed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing
    embed.add_field(name="", value="Scams are becoming a big problem on Discord servers. We are trying to limit the impact that experience whilst within our community.", inline=False)
    embed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing
    embed.add_field(name="", value="Please be considerate and respectful within our community.", inline=False)
    embed.add_field(name="", value="Help is given by Mysterium Wizards who are not paid to provide support and are members of the community like you.", inline=False)
    embed.add_field(name="", value="If you have an urgent issue that needs to be elevated to official support, the wizards or admin/moderators can escalate your issue for you or provide an email address where you can gain support.", inline=False)

    try:
        await member.send(embed=embed)
        print(f"Intro DM sent to new User {member.name}")
    except Exception as e:
        print(f'Could not send DM to {member.name}: {e}')
        print(f"New USER DM: {member.name} has DM turned off")

def setup(bot):
    bot.add_listener(on_member_join, "on_member_join")
