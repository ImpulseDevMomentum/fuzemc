import nextcord
from nextcord.ext import commands
import requests
from datetime import datetime

class MinecraftSkin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="skin", description="Fetch a Minecraft player's skin and profile information.")
    async def skin(self, interaction: nextcord.Interaction, username: str):
        playerdb_url = f"https://playerdb.co/api/player/minecraft/{username}"
        playerdb_response = requests.get(playerdb_url)

        if playerdb_response.status_code != 200:
            await interaction.response.send_message("Player not found.", ephemeral=True)
            return

        player_data = playerdb_response.json().get('data', {}).get('player', {})
        player_uuid = player_data.get('id', "Not available")
        player_name = player_data.get('username', "Not available")
        
        created_at = player_data.get('createdAt', None)
        if created_at:
            creation_date = datetime.utcfromtimestamp(created_at).strftime('%Y-%m-%d')
        else:
            creation_date = "Not available"

        name_history_url = f"https://api.mojang.com/user/profiles/{player_uuid}/names"
        name_history_response = requests.get(name_history_url)
        
        if name_history_response.status_code == 200:
            name_history = name_history_response.json()
            name_history_text = "\n".join([f"{name['name']} (changed on {datetime.utcfromtimestamp(name.get('changedToAt', 0)/1000).strftime('%Y-%m-%d')})" if 'changedToAt' in name else f"{name['name']} (original)" for name in name_history])
        else:
            name_history_text = "No history available."

        skin_url = f"https://mc-heads.net/body/{player_uuid}"

        embed = nextcord.Embed(
            title=f"{player_name}'s Minecraft Profile",
            description=f"Here is the Minecraft skin and profile information for {player_name}.",
            color=nextcord.Color.blue()
        )

        embed.set_image(url=skin_url)
        embed.add_field(name="Username", value=player_name, inline=True)
        embed.add_field(name="UUID", value=player_uuid, inline=True)
        embed.add_field(name="Account Creation Date", value=creation_date, inline=True)
        embed.add_field(name="Name History", value=name_history_text, inline=False)
        embed.set_footer(text="Data fetched from PlayerDB and Mojang API")

        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    if bot.get_cog('MinecraftSkin') is None:
        bot.add_cog(MinecraftSkin(bot))