import nextcord
from nextcord.ext import commands
import json
import os

class LastLetter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.json_file_path = 'last_letter_data.json'
        self.allowed_role_id = 1284274477542146068

    @nextcord.slash_command(name="change_last_letter", description="Change the last letter in the game.")
    async def change_last_letter(self, interaction: nextcord.Interaction, letter: str):
        if self.allowed_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        if len(letter) != 1 or not letter.isalpha():
            await interaction.response.send_message("Please provide a valid single letter.", ephemeral=True)
            return

        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {'last_letter': None}

        data['last_letter'] = letter.lower()

        with open(self.json_file_path, 'w') as f:
            json.dump(data, f)

        await interaction.response.send_message(f"The last letter has been changed to: {letter.upper()}", ephemeral=False)

def setup(bot):
    bot.add_cog(LastLetter(bot))