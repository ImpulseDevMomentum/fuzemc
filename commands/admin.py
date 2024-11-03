import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed, SelectOption
from nextcord.ui import View, Select
from datetime import datetime
from utils.allowed_users import *

class AdminRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="adminroles", description="Assign or remove an admin role.")
    async def adminroles(self, interaction: Interaction, channel: nextcord.TextChannel = SlashOption(description="Channel where the role selection embed will be sent")):
        if str(interaction.user.id) not in ALLOWED_USERS:
            await interaction.response.send_message("You can't use this command", ephemeral=True)
            return
        embed = Embed(
            title="🔧 Admin Role Selection",
            description="Select the role from the dropdown below. If you do not have the role, it will be assigned. If you already have the role, it will be removed.",
            color=nextcord.Color.blue(),
            timestamp=datetime.now()
        )

        embed.set_footer(text="Admin Role Management System")

        admin_role_options = Select(
            placeholder="Select a role to toggle",
            options=[
                SelectOption(label="Ticket Ping", description="Assign or remove the ticket ping", value="admin", emoji="<:contact:1284438035869728770>")
            ],
            custom_id="admin_role_selection"
        )

        view = View()
        view.add_item(admin_role_options)

        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"Role selection embed sent to {channel.mention}.", ephemeral=True)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction):
        if interaction.type == nextcord.InteractionType.component and interaction.data.get("custom_id") == "admin_role_selection":
            role_value = interaction.data['values'][0]
            await self.toggle_role(interaction, role_value)

    async def toggle_role(self, interaction: Interaction, role_value):
        member = interaction.user
        guild = interaction.guild
        admin_role_id = 1284441554458640478
        role = guild.get_role(admin_role_id)

        if role_value == "admin":
            if role in member.roles:
                await member.remove_roles(role)
                await interaction.response.send_message(f"The role {role.name} has been removed from you.", ephemeral=True)
            else:
                await member.add_roles(role)
                await interaction.response.send_message(f"You have been assigned the role {role.name}.", ephemeral=True)

def setup(bot):
    bot.add_cog(AdminRoles(bot))