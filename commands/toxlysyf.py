import nextcord, random
from nextcord.ext import commands

class FuzeMCCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ip", description="Responds with the server IP")
    async def ip(self, interaction: nextcord.Interaction):
        raniplist = ["ip1", "ip2", "ip3"]
        ranip = random.choice(raniplist)
        await interaction.response.send_message(f"IP: {ranip}", ephemeral=True)

    @nextcord.slash_command(name="version", description="Responds with the server version range")
    async def version(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Supported versions: x.x.x - x.x.x", ephemeral=True)

    @nextcord.slash_command(name="help", description="Provides a help link")
    async def help(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(
            "Help: link", 
            ephemeral=True
        )

    @nextcord.slash_command(name="shop", description="Redirects to the shop")
    async def shop(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Visit our shop: link", ephemeral=True)

    @nextcord.slash_command(name="itemshop", description="Redirects to the shop")
    async def itemshop(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Visit our shop: link", ephemeral=True)

def setup(bot):
    bot.add_cog(FuzeMCCommands(bot))
