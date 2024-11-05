import nextcord
from nextcord.ext import commands
from nextcord import Embed

class WelcomeMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1284517991652003862

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            print(f"Channel with ID {self.channel_id} not found.")
            return

        embed = Embed(
            title=":wave: Hello!",
            description=(
                f"Welcome, {member.mention} to the official Discord of server **server**\n\n"
                "**We hope that you will stay "
                "with us for more time!**\n\n"
                "> <#1234567890>\n"
                "> <#1234567890>\n\n"
                "<:fuzemc:1284520852334841909> server - Dive into the adventure with us and make lasting memories!"
            ),
            color=nextcord.Color.blue()
        )

        embed.set_thumbnail(url=member.avatar.url)

        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(WelcomeMessage(bot))
