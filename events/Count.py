import nextcord
from nextcord.ext import commands
import json
import os

class CountingGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1297153761323782144
        self.json_file_path = 'counting_data.json'

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.channel_id and not message.author.bot:
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, 'r') as f:
                    data = json.load(f)
            else:
                data = {'last_number': -1, 'last_user_id': None}

            data.setdefault('last_number', -1)
            data.setdefault('last_user_id', None)

            try:
                number = int(message.content)
            except ValueError:
                await message.delete()
                return

            if message.author.id == data['last_user_id']:
                await message.delete()
                return

            if number == data['last_number'] + 1:
                data['last_number'] = number
                data['last_user_id'] = message.author.id
                
                with open(self.json_file_path, 'w') as f:
                    json.dump(data, f)

                await message.delete()

                webhook = await self.get_webhook(message.channel)
                await webhook.send(
                    content=str(number),
                    username=message.author.display_name,
                    avatar_url=message.author.avatar.url if message.author.avatar else None
                )
            else:
                await message.delete()

    async def get_webhook(self, channel):
        if hasattr(self, 'webhook_cache') and channel.id in self.webhook_cache:
            return self.webhook_cache[channel.id]

        webhooks = await channel.webhooks()
        webhook = nextcord.utils.get(webhooks, name="CountingGame Webhook")
        if webhook is None:
            webhook = await channel.create_webhook(name="CountingGame Webhook")

        if not hasattr(self, 'webhook_cache'):
            self.webhook_cache = {}
        self.webhook_cache[channel.id] = webhook
        return webhook

def setup(bot):
    bot.add_cog(CountingGame(bot))