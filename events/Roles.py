import nextcord
from nextcord.ext import commands

class RoleNicknameManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        role_prefix_mapping = {
            1284275606506176714: "[H]",
            1284275479502782464: "[Jr Mod]",
            1284275278440562780: "[Mod]",
            1284274988320292894: "[Jr Admin]",
            1284274860067127360: "[Admin]"
        }

        added_roles = [role for role in after.roles if role not in before.roles]

        for role in added_roles:
            if role.id in role_prefix_mapping:
                prefix = role_prefix_mapping[role.id]
                display_name = after.display_name

                for existing_prefix in role_prefix_mapping.values():
                    if display_name.startswith(existing_prefix):
                        display_name = display_name[len(existing_prefix):].strip()

                new_nickname = f"{prefix} {display_name}"
                await after.edit(nick=new_nickname)

        removed_roles = [role for role in before.roles if role not in after.roles]
        if removed_roles:
            remaining_roles = [role for role in after.roles if role.id in role_prefix_mapping]
            if not remaining_roles:
                await after.edit(nick=None)

def setup(bot):
    bot.add_cog(RoleNicknameManager(bot))
