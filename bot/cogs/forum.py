import discord
from discord.ext import commands
from discord import app_commands as apc

class Forum(commands.GroupCog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @apc.command()
    @apc.choices(reason=[apc.Choice(name="Solved", value="A probléma meg lett oldva."),
                        apc.Choice(name="Több infó", value="Nem adtál meg elég információt. Kérlek, írd le részletesebben a problémát!"),
                        apc.Choice(name="Solved + fix", value="A probléma meg lett oldva, és a következő verzióban javítva lesz."),
                        apc.Choice(name="Más (adj meg jegyzetet is!)", value="Egyéb - kérlek, nézd meg a moderátor jegyzetét.")])
    @apc.rename(reason="indok")
    @apc.rename(note="megjegyzés")
    async def lock(self, interaction: discord.Interaction, reason: str, *, note: str = None):
        """Lezárja a fórumot. Csak fórum csatornákban működik.
        
        Parameters
        -----------
        reason: str
            A lezárás oka.
        note: str
            Egyéb megjegyzés."""
        if not 1149723882614444110 in [x.id for x in interaction.user.roles]:
            if not 1149724696028389487 in [x.id for x in interaction.user.roles]:
                if not 1112365433027313827 in [x.id for x in interaction.user.roles]:
                    return await interaction.response.send_message("Nincs jogosultságod ehhez a parancshoz.", ephemeral=True)
        if not isinstance(interaction.channel, discord.Thread):
            return await interaction.response.send_message("Ez a parancs csak fórum csatornákban működik.", ephemeral=True)
        if not note and reason == "Egyéb - kérlek, nézd meg a moderátor jegyzetét.":
            return await interaction.response.send_message("Egyéb indok esetén meg kell adnod egy megjegyzést is.", ephemeral=True)
        try:
            await interaction.channel.add_tags(discord.utils.get(interaction.channel.parent.available_tags, name="SOLVED"), reason="Megjelölve: Solved")
        except:
            return await interaction.response.send_message("Valószínűleg nincs elkészítve helyesen a 'SOLVED' címke! A bot a címke nevét keresi, fontos, hogy pontosan így nézzen ki: `SOLVED` (a nagybetűk és kisbetűk számítanak!)", ephemeral=True)
        await interaction.response.send_message(
            embed=discord.Embed(
            title="Lezárva",
            description=
                f"A poszt le lett zárva.\nIndok: {reason}\n\n{('Megjegyzés: ' + note if note else '')}",
            color=0xd8a044
            ).set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url, url="https://discord.com/users/" + str(interaction.user.id)))
        await interaction.channel.edit(locked=True, reason=reason, archived=True)
    
    @apc.command()
    async def priority(self, interaction: discord.Interaction):
        """PRIORITY megjelölése"""
        if not 1149723882614444110 in [x.id for x in interaction.user.roles]:
            if not 1149724696028389487 in [x.id for x in interaction.user.roles]:
                if not 1112365433027313827 in [x.id for x in interaction.user.roles]:
                    return await interaction.response.send_message("Nincs jogosultságod ehhez a parancshoz.", ephemeral=True)
        if not isinstance(interaction.channel, discord.Thread):
            return await interaction.response.send_message("Ez a parancs csak fórum csatornákban működik.", ephemeral=True)
        await interaction.channel.add_tags(discord.utils.get(interaction.channel.parent.available_tags, name="PRIORITY"), reason="Megjelölve: PRIORITY")
        await interaction.response.send_message(embed=discord.Embed(title="Megjelölve: Priority", color=0xd8a044))

async def setup(bot):
    await bot.add_cog(Forum(bot))