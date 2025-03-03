import discord
from discord import app_commands as apc
from discord.ext import commands

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await self.bot.tree.sync()
            await ctx.send(f"Reloaded `{cog}`")
        except Exception as e:
            await ctx.send(f"Error reloading `{cog}`:\n```{e}```")

async def setup(bot):
    await bot.add_cog(Reload(bot))
