import discord, xml.etree.ElementTree, random
from discord import app_commands as apc
from discord.ext import commands

class Insult(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__

    def check_piru(interaction):
        #if interaction.user.id == 648168353453572117: return None
        return apc.Cooldown(1, 120)

    @apc.command()
    @apc.checks.dynamic_cooldown(factory=check_piru)
    #@apc.checks.cooldown(1, 120, key=lambda i: i.user.id)
    async def insult(self, interaction, ping: discord.Member = None):
        """Inspired by kretainsult.online, szavak by DirtyWords.xml
        
        Parameters
        -----------
        ping: discord.Member
            A felhasználó, akit le akarsz szidni."""
        if not interaction.channel.id == 1210896959477522443:
            return await interaction.response.send_message("A parancsot csak a <#1210896959477522443> csatornában használhatod!", ephemeral=True)
        mainXml = xml.etree.ElementTree.parse("bot/DirtyWords.xml").getroot()
        nouns = [x.text.lower() for x in mainXml.findall("Word[@type='f']")]
        adjectives = [x.text.lower() for x in mainXml.findall("Word[@type='m']")]
        chooseInsultType = random.randint(1, 6)
        match chooseInsultType:
            case 1: insult = random.choice(nouns)
            case 2: insult = random.choice(adjectives)
            case 3: insult = random.choice(adjectives) + " " + random.choice(nouns)
            case 4: insult = random.choice(adjectives) + ", " + random.choice(adjectives) + " " + random.choice(nouns)
            case 5: insult = random.choice(nouns) + " " + random.choice(nouns)
            case 6: insult = random.choice(adjectives) + ", " + random.choice(adjectives) + ", " + random.choice(adjectives) + " " + random.choice(nouns)
        if random.randint(1, 1000) == 69:
            return await interaction.response.send_message(
                (f'({ping.mention}, ez az üzenet neked is szól.)\n\n' if ping else "") + f"Miért szereti az ember bántani a többieket? Tán azért, mert egoista? Esetleg azért, hogy megmutassa, ő a dominánsabb? Esetleg mert öntelt? Ezek közül egyik válasz sem helyes.\n\nAz ember azért bántja a többieket, mert ahhoz van kedve. Igen, ez furának hangozhat, hiszen ott vannak például a turret-szindrómások, akik néha úgy káromkodnak, hogy nincsen sértő szándékuk. De nagy a különbség a káromkodás és a bántás között.\nHa te most odamész egy random emberhez az utszán, és odaordítod neki, hogy \"Te {random.choice(nouns)}!\", szerinted mivel lesz jobb a napja? Semmivel. És a tiéd? Szintén semmivel. Meg kell tanulni, hogy hol a határ, és nem szabad másokon kiengedni a dühödet, még akkor sem, ha rosszat csinált. Nyilván az ember általában nem direkt tesz olyan dolgokat, amikkel más embereket akar megsérteni. Ha meg igen, akkor\n# rohadjon el a büdös názáreti gecifolyóba, a kis {random.choice(nouns)}, kurva anyád, te {insult}!")
        await interaction.response.send_message((ping.mention + "\n" if ping else "") + random.choice(["Hogy rohadnál meg, te ", "Te "]) + insult + "!")

async def setup(bot):
    await bot.add_cog(Insult(bot))
