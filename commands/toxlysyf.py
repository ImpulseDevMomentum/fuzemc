import nextcord, random
from nextcord.ext import commands

class FuzeMCCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ip", description="Responds with the server IP")
    async def ip(self, interaction: nextcord.Interaction):
        raniplist = ["fuzemc.pl", "fuzemc.net", "fuzemc.eu"]
        ranip = random.choice(raniplist)
        await interaction.response.send_message(f"IP: {ranip}", ephemeral=True)

    @nextcord.slash_command(name="version", description="Responds with the server version range")
    async def version(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Supported versions: 1.8.8 - 1.21.1", ephemeral=True)

    @nextcord.slash_command(name="help", description="Provides a help link")
    async def help(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(
            "Help: https://discord.com/channels/1283713732387799060/1283728453383753741/1284448855756374078", 
            ephemeral=True
        )

    @nextcord.slash_command(name="shop", description="Redirects to the shop")
    async def shop(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Visit our shop: https://fuzemc.net", ephemeral=True)

    @nextcord.slash_command(name="itemshop", description="Redirects to the shop")
    async def itemshop(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Visit our shop: https://fuzemc.net", ephemeral=True)

def setup(bot):
    bot.add_cog(FuzeMCCommands(bot))