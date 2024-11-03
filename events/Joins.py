import nextcord
from nextcord.ext import commands

class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        role_id = 1283723516323299411

        role = member.guild.get_role(role_id)
        if role:
            try:
                await member.add_roles(role)
                print(f"Role {role.name} has been added to {member.name}.")
            except Exception as e:
                print(f"There was a problem to add role to {member.name}: {e}")
        else:
            print(f"Role ID {role_id} couldnt be found {member.guild.name}.")

def setup(bot):
    bot.add_cog(MemberJoin(bot))