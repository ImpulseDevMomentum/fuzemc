import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle
from nextcord.ui import Button, View, Modal, TextInput
from utils.allowed_users import *
import random

class MathVerificationModal(Modal):
    def __init__(self, interaction: Interaction, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interaction = interaction

        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)

        self.math_input = TextInput(
            label=f"What is {self.num1} + {self.num2}?",
            placeholder="Enter your answer",
            required=True,
        )
        self.add_item(self.math_input)

    async def callback(self, interaction: Interaction):
        correct_answer = self.num1 + self.num2

        try:
            user_answer = int(self.math_input.value)
        except ValueError:
            await interaction.response.send_message("Please enter a valid number.", ephemeral=True)
            return

        if user_answer == correct_answer:
            verified_role = interaction.guild.get_role(1283719790091042878)
            unverified_role = interaction.guild.get_role(1283723516323299411)

            await interaction.user.add_roles(verified_role)
            if unverified_role:
                await interaction.user.remove_roles(unverified_role)

            await interaction.response.send_message(f"🎉 You have been verified and received the role {verified_role.mention} !", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Incorrect answer. Please try again.", ephemeral=True)

class MathVerificationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="verify", description="Send a verification embed to a specified channel")
    async def verify(self, interaction: Interaction, channel: nextcord.TextChannel):
        if str(interaction.user.id) not in ALLOWED_USERS:
            await interaction.response.send_message("You can't use this command", ephemeral=True)
            return
        embed = nextcord.Embed(
            title="✅ Verification",
            description="Click the button below to verify your account",
            color=nextcord.Color.green()
        )

        embed.set_footer(text="Click the button to complete verification")

        button = Button(label="Verify Me", style=ButtonStyle.green, custom_id="verify_user", emoji="<:verification:1284452916807340064>")

        view = View(timeout=None)
        view.add_item(button)

        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"✅ Verification embed sent to {channel.mention}!", ephemeral=True)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction):
        if interaction.type == nextcord.InteractionType.component and interaction.data["custom_id"] == "verify_user":
            modal = MathVerificationModal(title="Math Verification", interaction=interaction)
            await interaction.response.send_modal(modal)

def setup(bot):
    bot.add_cog(MathVerificationCog(bot))