import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Permissions
from utils.allowed_users import ALLOWED_USERS

class TicketManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="user", description="Manage ticket permissions.")
    async def ticket(self, interaction: Interaction):
        pass

    @ticket.subcommand(name="add", description="Grant access to a ticket channel.")
    async def ticket_add(self, interaction: Interaction, user: nextcord.User = SlashOption(description="User to add to the ticket")):
        if not self._has_permission(interaction.user):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        channel = interaction.channel
        if self._is_ticket_channel(channel):
            await channel.set_permissions(user, read_messages=True, send_messages=True)
            await interaction.response.send_message(f"{user.mention} has been granted access to this ticket channel.", ephemeral=True)
        else:
            await interaction.response.send_message("This channel is not a recognized ticket channel.", ephemeral=True)

    @ticket.subcommand(name="remove", description="Remove access from a ticket channel.")
    async def ticket_remove(self, interaction: Interaction, user: nextcord.User = SlashOption(description="User to remove from the ticket")):
        if not self._has_permission(interaction.user):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        channel = interaction.channel
        if self._is_ticket_channel(channel):
            await channel.set_permissions(user, read_messages=False, send_messages=False)
            await interaction.response.send_message(f"{user.mention} has been removed from this ticket channel.", ephemeral=True)
        else:
            await interaction.response.send_message("This channel is not a recognized ticket channel.", ephemeral=True)

    def _is_ticket_channel(self, channel: nextcord.TextChannel) -> bool:
        valid_names = ["help", "partnership", "contact", "bug", "player_report"]
        return any(name in channel.name.lower() for name in valid_names)

    def _has_permission(self, user: nextcord.User) -> bool:
        ALLOWED_USERS = ["1122846756124774470", "1030566399283826698"]
        return str(user.id) in ALLOWED_USERS

def setup(bot):
    bot.add_cog(TicketManagement(bot))