import discord, discord.app_commands as apc, random
from discord.ext import commands
    
class TOTW(commands.GroupCog, name="totw"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @apc.command()
    async def set(self, interaction: discord.Interaction, link: str):
        """A Hét Témájának kiválasztása.
        
        Parameters
        -----------
        link: str
            A fórum poszt linkje.
        """
        if not 1149723882614444110 in [x.id for x in interaction.user.roles]: return await interaction.response.send_message("Nincs jogosultságod ehhez a parancshoz.", ephemeral=True)
        link = link.split("/")
        try:
            channel = await interaction.guild.fetch_channel(int(link[-1]))
        except:
            return await interaction.response.send_message("Nincs ilyen csatorna! Fontos, hogy ne üzenet linked adj meg, hanem fórum poszt linket.", ephemeral=True)
        if type(channel) != discord.Thread: return await interaction.response.send_message("Ez nem fórum poszt!", ephemeral=True)
        try:
            await channel.add_tags(discord.utils.get(channel.parent.available_tags, name="Hét Témája"), reason="TOTW nyertes")
        except:
            return await interaction.response.send_message("Nincs elkészítve helyesen a 'Hét Témája' címke! A bot a címke nevét keresi, fontos, hogy pontosan így nézzen ki: `Hét Témája` (a nagybetűk és kisbetűk számítanak!)", ephemeral=True)
        author = channel.owner
        role = discord.utils.get(interaction.guild.roles, name="Hét Témája")
        if role is None: return await interaction.response.send_message("Nincs elkészítve helyesen a 'Hét Témája' rang! A bot a rang nevét keresi, fontos, hogy pontosan így nézzen ki: `Hét Témája` (a nagybetűk és kisbetűk számítanak!)", ephemeral=True)
        await role.edit(color=discord.Color.from_str("#d8a044"))
        for i in role.members:
            await i.remove_roles(role, reason="TOTW lejárt")
        try:
            await author.add_roles(role, reason="TOTW nyertes")
        except discord.Forbidden:
            return await interaction.response.send_message("Nincs jogom ehhez! A Firka Bot rangja legyen az 'A Hét Témája' rang fölött!", ephemeral=True)
        newname = "🏆 " + channel.name if not channel.name.startswith("🏆") else channel.name
        for i in channel.parent.threads:
            if i.flags.pinned:
                await i.edit(pinned=False)
        await channel.edit(pinned=True, name=newname if len(newname) < 100 else channel.name)
        sent = True
        try:
            await author.send(
f"""# {random.choice(['Szép munka', 'Gratulálok', 'Ügyes vagy', 'GG', 'Szép volt', 'Wow', 'Azta'])}, {author.global_name}!
## A te posztod ({channel.mention}) nyerte meg a Hét Témája versenyt!
A jutalmad a `Hét Témája` rang egy hétre!

Parancsok a rangod szerkesztéséhez:
- `/totw color <hex kód>`: a rang színének beállítása
- `/totw icon <link/emoji>`: a rang ikonjának beállítása

_A posztod egy hétig ki lesz tűzve a <#1153062349004083241> fórumba. A rang (akkor is, ha collabból készült a téma), csak a poszt készítőjén lehet._
_A rangot átruházni másra nem lehet, ez egy kinevezés._
_Ezek mellett a poszt megkapta örökre a `Hét Témája` címkét, és a `🏆` prefixet._""")
        except discord.Forbidden:
            sent = False
        embed = discord.Embed(title="Ez a poszt lett A HÉT TÉMÁJA!", description=f"Gratulálunk, {author.mention}!\nA jutalmad a {role.mention} rang egy hétre!", colour=0xd8a044)
        embed.set_footer(text=("Nem tudtunk privát üzenetet küldeni :(" if not sent else "Küldtünk néhány információt privátban :)"))
        await channel.send(content=author.mention if not sent else None, embed=embed)
        await interaction.response.send_message("A Hét Témája sikeresen ki lett választva!")

    @apc.command()
    async def color(self, interaction, color: str):
        """Beállítja a Hét Témája rang színét.
        
        Parameters
        -----------
        color: str
            A szín hex kódja.
        """
        role: discord.Role = discord.utils.get(interaction.guild.roles, name="Hét Témája")
        if not interaction.user in role.members: return await interaction.response.send_message("Nincs jogod ehhez!", ephemeral=True)
        if color.startswith("#"): color = color[1:]
        if role is None: return await interaction.response.send_message("Nincs elkészítve helyesen az 'A Hét Témája' rang! Keress fel egy csapattagot!", ephemeral=True)
        try:
            await role.edit(colour=discord.Colour(int(color, 16)))
        except discord.Forbidden:
            return await interaction.response.send_message("Nincs jogom ehhez! Keress fel egy csapattagot!", ephemeral=True)
        await interaction.response.send_message(f"A szín sikeresen be lett állítva a `#{color.upper()}` színre!\n{role.mention}")
    
    @apc.command()
    async def icon(self, interaction: discord.Interaction, link: str = None, emoji: str = None):
        """Beállítja a Hét Témája rang ikonját. (link VAGY emoji)
        
        Parameters
        -----------
        link: str
            A kép linkje. (opcionális)
        emoji: str
            Az emoji neve. (opcionális)
        """
        if not interaction.guild.premium_tier >= 2:
            return await interaction.response.send_message("A szervernek legalább 2. szintűnek kell lennie! Bocsi :(", ephemeral=True)
        role: discord.Role = discord.utils.get(interaction.guild.roles, name="Hét Témája")
        if not interaction.user in role.members: return await interaction.response.send_message("Nincs jogod ehhez!", ephemeral=True)
        if role is None: return await interaction.response.send_message("Nincs elkészítve helyesen az 'A Hét Témája' rang! Keress fel egy csapattagot!", ephemeral=True)
        if link:
            try:
                await role.edit(display_icon=link)
            except discord.Forbidden:
                return await interaction.response.send_message("Nincs jogom ehhez! Keress fel egy csapattagot!", ephemeral=True)
            except discord.HTTPException:
                return await interaction.response.send_message("Hibás linket adtál meg! A kompatibilitás kedvéért adj meg egy Discordos CDN-linket (jobbklikk egy képre -> link másolása)", ephemeral=True)
            await interaction.response.send_message(f"Az ikon sikeresen be lett állítva!")
        elif emoji:
            try:
                await role.edit(display_icon=emoji)
            except discord.Forbidden:
                return await interaction.response.send_message("Nincs jogom ehhez! Keress fel egy csapattagot!", ephemeral=True)
            await interaction.response.send_message(f"Az ikon sikeresen be lett állítva!")
        else:
            await interaction.response.send_message("Nem adtál meg linket vagy emojit!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TOTW(bot))
