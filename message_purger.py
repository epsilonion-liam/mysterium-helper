import nextcord
from nextcord.ext import commands
print(f'Message Purger Plugin Loaded')
async def purge_user_messages(ctx, member: nextcord.Member):
    if any(role.name in ["admin", "mods", "mysterium wizards", "pro wizard"] for role in ctx.author.roles):
        await ctx.channel.purge(limit=None, check=lambda m: m.author == member)
        await ctx.send(f"Purged messages from {member.mention}.")
        log_channel = nextcord.utils.get(ctx.guild.channels, name='logs')
        if log_channel:
            await log_channel.send(f"{ctx.author} purged messages from {member}.")
    else:
        await ctx.send("You do not have permission to use this command.")

def setup(bot):
    bot.add_command(commands.Command(purge_user_messages, name="purge"))
