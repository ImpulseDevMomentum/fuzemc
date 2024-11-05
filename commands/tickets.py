import nextcord
from nextcord.ext import commands
from nextcord import ButtonStyle, Embed, Interaction, SlashOption, SelectOption, Member
from nextcord.ui import Button, View, Select, Modal, TextInput
from datetime import datetime
import json, os
from utils.allowed_users import *

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 1234567890 # Paste your channel id here ( If you don't know how to do this, look it up on youtube )
        self.ticket_data_file = 'ticket_data.json'
        self.transcript_folder = 'transcripts'
        
        if not os.path.exists(self.ticket_data_file):
            with open(self.ticket_data_file, 'w') as f:
                json.dump({}, f)
                
        if not os.path.exists(self.transcript_folder):
            os.makedirs(self.transcript_folder)

    def load_ticket_data(self):
        with open(self.ticket_data_file, 'r') as f:
            return json.load(f)

    def save_ticket_data(self, data):
        with open(self.ticket_data_file, 'w') as f:
            json.dump(data, f)

    def get_next_ticket_number(self, category_value):
        data = self.load_ticket_data()
        if category_value not in data:
            data[category_value] = 0
        data[category_value] += 1
        self.save_ticket_data(data)
        return data[category_value]

    @nextcord.slash_command(name="ticket", description="Start the ticket system")
    async def ticket(self, interaction: Interaction, channel: nextcord.TextChannel = SlashOption(description="Channel where the button will be sent")):
        if str(interaction.user.id) not in ALLOWED_USERS:
            await interaction.response.send_message("You can't use this command", ephemeral=True)
            return
        embed = Embed(
            title="🎫 Ticket System",
            description="Welcome to the ticket system! Please select a category and fill out the form to create a ticket. Our team will assist you as soon as possible.",
            color=nextcord.Color.blue()
        )

        embed.add_field(name="Categories", value=(
            "🔹 **I Need Help**: Request general assistance.\n"
            "🔹 **Partnership**: Discuss potential partnerships.\n"
            "🔹 **Contact**: Get in touch with the team.\n"
            "🔹 **Report a Bug**: Report any technical issues.\n"
            "🔹 **Report a Player**: Report a player’s behavior."
        ), inline=False)

        embed.set_footer(text="Thank you for reaching out! We’re here to help.")

        categories = Select(
            placeholder="Select a category",
            options=[
                SelectOption(label="I Need Help", description="Request assistance", value="help", emoji="❓"),
                SelectOption(label="Partnership", description="Discuss partnerships", value="partnership", emoji="🤝"),
                SelectOption(label="Contact", description="Contact the team", value="contact", emoji="📞"),
                SelectOption(label="Report a Bug", description="Report a technical issue", value="bug", emoji="🐞"),
                SelectOption(label="Report a Player", description="Report a player", value="player_report", emoji="🚨")
            ],
            custom_id="ticket_category"
        )

        view = View()
        view.add_item(categories)

        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"Embed sent to {channel.mention}.", ephemeral=True)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction):
        if interaction.type == nextcord.InteractionType.component:
            custom_id = interaction.data.get("custom_id")

            if custom_id == "ticket_category":
                category_value = interaction.data['values'][0]
                await self.show_modal_for_category(interaction, category_value)

            elif custom_id == "close_ticket":
                await self.on_close_ticket(interaction)

    async def show_modal_for_category(self, interaction: Interaction, category_value: str):
        """Display appropriate modal based on selected category."""
        if category_value == "help":
            modal = HelpModal()
        elif category_value == "partnership":
            modal = PartnershipModal()
        elif category_value == "contact":
            modal = ContactModal()
        elif category_value == "bug":
            modal = BugModal()
        elif category_value == "player_report":
            modal = PlayerReportModal()
        else:
            return
        await interaction.response.send_modal(modal)

    async def create_ticket(self, interaction: Interaction, category_value, form_data):
        """Create a ticket channel based on the provided data."""
        author = interaction.user
        guild = interaction.guild
        await interaction.response.defer()

        # Role permissions based on the category
        role_mapping = {
            "help": [1284275606506176714, 1284275479502782464, 1284275278440562780, 1284274988320292894, 1284274860067127360, 1284274731284959356],
            "partnership": [1284274477542146068],
            "contact": [1284275278440562780, 1284274988320292894, 1284274860067127360, 1284274731284959356],
            "bug": [1284274860067127360, 1284274731284959356],
            "player_report": [1284275606506176714, 1284275479502782464, 1284275278440562780, 1284274988320292894, 1284274860067127360, 1284274731284959356]
        }
        selected_roles = role_mapping.get(category_value, [])

        ticket_number = self.get_next_ticket_number(category_value)
        ticket_channel = await guild.create_text_channel(f"{category_value}-{ticket_number}", category=None)

        for role_id in selected_roles:
            role = guild.get_role(role_id)
            if role:
                await ticket_channel.set_permissions(role, read_messages=True, send_messages=True, read_message_history=True)

        await ticket_channel.set_permissions(author, read_messages=True, send_messages=True, read_message_history=True)
        await ticket_channel.set_permissions(guild.default_role, view_channel=False)

        await self.send_ticket_details(ticket_channel, category_value, author, form_data)
        await interaction.followup.send(f"Your ticket was created: {ticket_channel.mention}", ephemeral=True)

    async def send_ticket_details(self, channel, category_value, author, form_data):
        creation_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

        # Notify staff and user
        await channel.send(f"||{author.mention} <@&1284441554458640478>||")

        embed = Embed(
            title="🎫 Ticket Created",
            description=f"Category: **{category_value.replace('_', ' ').title()}**\nUser: {author.mention}\nCreation Time: **{creation_time}**\n\n{form_data}\n\n<:warning:1284458073607635056> Our team will attend to your ticket shortly.",
            color=nextcord.Color.green()
        )

        close_button = Button(label="Close Ticket", style=ButtonStyle.red, custom_id="close_ticket")
        view = View()
        view.add_item(close_button)

        await channel.send(embed=embed, view=view)

    async def on_close_ticket(self, interaction: Interaction):
        channel = interaction.channel
        user_roles = [role.id for role in interaction.user.roles]
        allowed_roles = [1284275606506176714, 1284275479502782464, 1284275278440562780, 1284274988320292894, 1284274860067127360, 1284274731284959356, 1284274477542146068]

        if any(role in allowed_roles for role in user_roles):
            transcript_file = await self.generate_transcript(channel)

            log_embed = Embed(
                title="🎫 Ticket Closed",
                description=f"Ticket in channel {channel.mention} has been closed.",
                color=nextcord.Color.red(),
                timestamp=datetime.utcnow()
            )

            log_channel = self.bot.get_channel(self.log_channel_id)
            if log_channel:
                await log_channel.send(embed=log_embed)
                await log_channel.send(file=transcript_file)

            await channel.send(f"Ticket closed. Thank you for your patience.")
            await channel.delete()
        else:
            await interaction.response.send_message("You do not have permission to close this ticket.", ephemeral=True)

    async def generate_transcript(self, channel):
        """Generate transcript from the channel's messages."""
        messages = await channel.history(limit=None, oldest_first=True).flatten()
        transcript_content = f"Transcript of {channel.name}\n\n"

        for message in messages:
            timestamp = message.created_at.strftime('%d-%m-%Y %H:%M:%S')
            transcript_content += f"{timestamp} - {message.author.display_name}: {message.content}\n"

        transcript_file_path = os.path.join(self.transcript_folder, f"{channel.name}_transcript.txt")
        with open(transcript_file_path, 'w') as f:
            f.write(transcript_content)

        return nextcord.File(transcript_file_path)


class HelpModal(Modal):
    def __init__(self):
        super().__init__(title="I Need Help")

        self.username = TextInput(label="Minecraft Username", required=True)
        self.minigame = TextInput(label="Game Mode / Minigame", required=True)
        self.description = TextInput(label="Description", style=nextcord.TextInputStyle.paragraph, required=True)

        self.add_item(self.username)
        self.add_item(self.minigame)
        self.add_item(self.description)

    async def callback(self, interaction: Interaction):
        form_data = f"**<:username:1284457521779703910> Username**: ```{self.username.value}```\n\n**<:gamemode:1284457443774169170> Game Mode**: ```{self.minigame.value}```\n\n**<:description:1284457491991760957> Description**: ```{self.description.value}```"
        cog = interaction.client.get_cog("TicketSystem")
        await cog.create_ticket(interaction, "help", form_data)


class PartnershipModal(Modal):
    def __init__(self):
        super().__init__(title="Partnership Request")

        self.type = TextInput(label="Partnership Type", required=True)
        self.link = TextInput(label="Discord Link / Website", required=True)
        self.description = TextInput(label="Description", style=nextcord.TextInputStyle.paragraph, required=True)

        self.add_item(self.type)
        self.add_item(self.link)
        self.add_item(self.description)

    async def callback(self, interaction: Interaction):
        form_data = f"**<:partnership:1284437620935622657> Partnership Type**: ```{self.type.value}```\n\n**<:link:1284458628752867429> Link**: ```{self.link.value}```\n\n**<:description:1284457491991760957> Description**: ```{self.description.value}```"
        cog = interaction.client.get_cog("TicketSystem")
        await cog.create_ticket(interaction, "partnership", form_data)


class ContactModal(Modal):
    def __init__(self):
        super().__init__(title="Contact")

        self.description = TextInput(label="Description", style=nextcord.TextInputStyle.paragraph, required=True)

        self.add_item(self.description)

    async def callback(self, interaction: Interaction):
        form_data = f"**<:description:1284457491991760957> Description**: ```{self.description.value}```"
        cog = interaction.client.get_cog("TicketSystem")
        await cog.create_ticket(interaction, "contact", form_data)


class BugModal(Modal):
    def __init__(self):
        super().__init__(title="Bug Report")

        self.gamemode = TextInput(label="Game Mode / Minigame", required=True)
        self.version = TextInput(label="Client Version", required=True)
        self.description = TextInput(label="Description of the Bug", style=nextcord.TextInputStyle.paragraph, required=True)

        self.add_item(self.gamemode)
        self.add_item(self.version)
        self.add_item(self.description)

    async def callback(self, interaction: Interaction):
        form_data = f"**<:gamemode:1284457443774169170> Game Mode**: ```{self.gamemode.value}```\n\n**<:version:1284458527414292592> Client Version**: ```{self.version.value}```\n\n**<:description:1284457491991760957> Description**: ```{self.description.value}```"
        cog = interaction.client.get_cog("TicketSystem")
        await cog.create_ticket(interaction, "bug", form_data)


class PlayerReportModal(Modal):
    def __init__(self):
        super().__init__(title="Player Report")

        self.username = TextInput(label="Minecraft Username", required=True)
        self.reported_user = TextInput(label="Reported Player", required=True)
        self.gamemode = TextInput(label="Game Mode / Minigame", required=True)
        self.description = TextInput(label="Description of Incident", style=nextcord.TextInputStyle.paragraph, required=True)

        self.add_item(self.username)
        self.add_item(self.reported_user)
        self.add_item(self.gamemode)
        self.add_item(self.description)

    async def callback(self, interaction: Interaction):
        form_data = f"**<:username:1284457521779703910> Player's Minecraft Username**: ```{self.username.value}```\n\n**<:reported:1284457468545728524> Reported Player's Username**: ```{self.reported_user.value}```\n\n**<:gamemode:1284457443774169170> Game Mode**: ```{self.gamemode.value}```\n\n**<:description:1284457491991760957> Description**: ```{self.description.value}```"
        cog = interaction.client.get_cog("TicketSystem")
        await cog.create_ticket(interaction, "player_report", form_data)

def setup(bot):
    bot.add_cog(TicketSystem(bot))
