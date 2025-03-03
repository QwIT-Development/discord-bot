import discord
from discord import app_commands as apc
from discord.ext import commands

class Tags(discord.ext.commands.GroupCog, name="tag"):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Tags(bot))
