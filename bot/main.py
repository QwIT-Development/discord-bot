import discord, os, dotenv, platform, asyncio, sqlite3 as sql
from discord.ext import commands
dotenv.load_dotenv("./.env")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all(), activity=discord.CustomActivity(name="🌐 https://firka.app/"))
        self.db = sql.connect("bot/database.db")
        self.db.execute("CREATE TABLE IF NOT EXISTS gh (tag TEXT)")
        self.remove_command("help")
    
    async def setup_hook(self):
        for i in os.listdir("bot/cogs"):
            if i.endswith(".py"):
                await self.load_extension(f"cogs.{i[:-3]}")
        await self.tree.sync()
        print(f'Bot is ready.\nCommands: {["/" + x.name for x in self.tree.get_commands()]}\nServers: {[x.name + " - " + str(x.id) for x in self.guilds]}')

    async def on_error(self, error, ctx):
        if isinstance(error, commands.NotOwner):
            await ctx.send("Nincs jogod ehhez!", delete_after=3)
        else:
            await ctx.send(f"Hiba lépett fel. Kérlek, jelezd a csapatunknak.\n```{error}```", delete_after=10)
bot = Bot()

@bot.tree.error 
async def on_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"Kérlek, várj még **{round(error.retry_after)}** másodpercet.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Hiba lépett fel. Kérlek, jelezd a csapatunknak.\n```{error}```", ephemeral=True)
        raise error

if "Windows" in platform.system():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    bot.run(os.getenv("DEBUGTOKEN"))
else:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    bot.run(os.getenv("TOKEN"))
