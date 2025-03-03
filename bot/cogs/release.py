import discord, requests, datetime
from discord import app_commands as apc
from discord.ext import commands

class Release(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @apc.command()
    async def release(self, interaction, csatorna: discord.TextChannel = None):
        """Legújabb verzió posztolása.
        
        Parameters
        -----------
        csatorna: discord.TextChannel
            A csatorna, ahova posztolni akarod. (alap csatorna a hírek)"""
        if not 1144647901520351232 in [x.id for x in interaction.user.roles]: return await interaction.response.send_message("Nincs jogosultságod ehhez a parancshoz.", ephemeral=True)
        csatorna = csatorna or await self.bot.fetch_channel(1111781560543363135)
        result = requests.get("https://api.github.com/repos/QwIT-Development/app-legacy/releases").json()
        result = result[0]
        latest = self.bot.db.execute("SELECT tag FROM gh").fetchone()
        if latest and result["tag_name"] == latest[0]:
            release_view = ReleaseView(result, csatorna)
            await interaction.response.send_message("Ez a verzió már ki lett adva. Biztosan kiposztolod?", ephemeral=True, view=release_view)
            release_view.response = await interaction.original_response()
            return
        self.bot.db.execute("UPDATE gh SET tag = ?", (result["tag_name"],))
        self.bot.db.commit()
        embed = discord.Embed(
            title=result["name"],
            description=result["body"].replace("\r\n", "\n"),
            timestamp=datetime.datetime.now(),
            colour=0x7ca021,
            url=result["html_url"]
        )
        embed.set_author(name="@" + result["author"]["login"], icon_url=result["author"]["avatar_url"], url=result["author"]["url"])
        view = discord.ui.View()
        link = discord.ui.Button(label="Letöltés", url=result["html_url"], style=discord.ButtonStyle.grey)
        view.add_item(link)
        await csatorna.send(embed=embed, view=view, content="<@&1171032910141329439>")
        await interaction.response.send_message("Kiposztolva!", ephemeral=True)

class ReleaseView(discord.ui.View):
    def __init__(self, data, channel):
        self.data=data
        self.channel=channel
        self.response = None
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Igen", style=discord.ButtonStyle.green)
    async def post_release(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=self.data["name"],
            description=self.data["body"].replace("\r\n", "\n"),
            timestamp=datetime.datetime.now(),
            colour=0x7ca021,
            url=self.data["html_url"]
        )
        embed.set_author(name="@" + self.data["author"]["login"], icon_url=self.data["author"]["avatar_url"], url=self.data["author"]["url"])
        view = discord.ui.View()
        link = discord.ui.Button(label="Letöltés", url=self.data["html_url"], style=discord.ButtonStyle.grey)
        view.add_item(link)
        await self.channel.send(embed=embed, view=view)
        for i in self.children: i.disabled = True
        return await interaction.response.edit_message(content="Kiposztolva!", view=self)

    @discord.ui.button(label="Nem", style=discord.ButtonStyle.red)
    async def dont_post_release(self, interaction: discord.Interaction, button: discord.ui.Button):
        for i in self.children: i.disabled = True
        return await interaction.response.edit_message(content="pussy", view=self)

async def setup(bot):
    await bot.add_cog(Release(bot))
