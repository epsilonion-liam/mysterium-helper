import nextcord
from nextcord.ext import commands

print(f'Custom Commands Plugin Loaded')
def setup(bot):
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
        await ctx.send('It is easy to stake and withdraw your stake follow these simple staps:\n 1. Go to https://app.iq.space/\n2. Connect your MetaMask wallet\n3. Deposit MYST token\nYou will need a small amount of POL (was Matic) for gas fees.\n\n If you get an error about your limits visit https://revoke.cash/ connect your wallet and set a new limit if needed')

    @bot.command(name="nodesafety")
    async def nodesafety(ctx):
        await ctx.send('Follow the link below to read on running an exit node and how to protect yourself\n https://help.mystnodes.com/en/articles/8005105-can-my-node-be-used-for-illegal-activities-how-do-we-protect-node-runners\n https://dvpnalliance.org/exit-node/\nAny further questions can be asked at help@mysterium.network')

    @bot.command(name="mystopennat")
    async def mystopennat(ctx):
        await ctx.send('You can achieve open NAT by manually forwarding ports as described in the article linked\nhttps://help.mystnodes.com/en/articles/8005269-manual-port-forwarding')

    @bot.command(name="nodequality")
    async def nodequality(ctx):
        await ctx.send('Enter this URL in your browser and replace nodeID with your node ID https://discovery.mysterium.network/api/v3/proposals?&access_policy=all&provider_id=<your_nodes_ID_Here>')

    @bot.command(name="help")
    async def help_command(ctx):
        helpembed = nextcord.Embed(title="Mysterium Helper v0.9.1", description="Written by Liam Gibbins AKA epsilonion, this bot has been created and will be updated with new features as requests from the community come in.\n The bot is aimed to combat spam and help the community with any issue that they may need help for. \n I would like to thank Adine for his work on the API endpoints that have been adapted for use on the bot. \n\n Road map -\n * To display current token price with daily shift to be added to the !stats command \n * Add more stats to the !stats custom command such as current Fee etc \n * Read file lists for blocked URLs", color=0x00ff00)
        helpembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1293610332090007553/1293610365380198483/00002-3113208706.png?ex=67080009&is=6706ae89&hm=eb77b4a04fa5060da0a921b4699f025ce65ce701700cba1886f7fc87d910b668&")
        helpembed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing
        helpembed.add_field(name="Features of this bot", value="* Sends a DM to new server members with important information about DM support scams and community guidelines. \n * Removes spam invites for support and bans after 3 warnings except admin, mod, mysterium wizard and pro wizard roles. \n * Custom commands for supplying easy support for frequent questions. \n * Adult word censoring. \n * Displays Node Quality stats with the !nodestats <nodeID> custom command \n * Display Networks statsistics with the !stats custom command", inline=False)
        helpembed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing
        helpembed.add_field(name="", value="Custom Commands", inline=False)
        helpembed.add_field(name="!nodestats", value="!node <API Key> displays node quality stats", inline=False)
        helpembed.add_field(name="!stats", value="Displays Network stats", inline=False)
        helpembed.add_field(name="!rundocker", value="Displays a link to my.mystnodes help page", inline=False)
        helpembed.add_field(name="!runlinux", value="Displays a link to my.mystnodes help page", inline=False)
        helpembed.add_field(name="!backupid", value="Displays a link to my.mystnodes help page", inline=False)
        helpembed.add_field(name="!stakingmyst", value="Displays a link to my.mystnodes help page", inline=False)
        helpembed.add_field(name="!nodesafety", value="Displays a link to my.mystnodes help page", inline=False)
        helpembed.add_field(name="!mystopennat", value="Displays a link to my.mystnodes help page", inline=False) 
        helpembed.add_field(name="\u200B", value="\u200B", inline=False)  # Blank line for spacing
        await ctx.send(embed=helpembed)
