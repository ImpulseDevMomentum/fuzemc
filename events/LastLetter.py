import nextcord
from nextcord.ext import commands
import json
import os

class LastLetterGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1297153780017660026
        self.json_file_path = 'last_letter_data.json'
        self.webhook_cache = {}

    async def get_webhook(self, channel):
        if channel.id in self.webhook_cache:
            return self.webhook_cache[channel.id]

        webhooks = await channel.webhooks()
        
        webhook = nextcord.utils.get(webhooks, name="FuzeMC - LastLetter")
        if webhook is None:
            webhook = await channel.create_webhook(name="FuzeMC - LastLetter")
        
        self.webhook_cache[channel.id] = webhook
        return webhook

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.channel_id and not message.author.bot:
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, 'r') as f:
                    data = json.load(f)
            else:
                data = {'last_letter': None}

            data.setdefault('last_letter', None)

            word = message.content.strip().lower()
            if not word.isalpha():
                await message.delete()
                return

            if data['last_letter'] is None or word[0] == data['last_letter']:
                data['last_letter'] = word[-1]
                
                with open(self.json_file_path, 'w') as f:
                    json.dump(data, f)

                await message.delete()

                webhook = await self.get_webhook(message.channel)

                await webhook.send(
                    content=word,
                    username=message.author.display_name,
                    avatar_url=message.author.avatar.url if message.author.avatar else None
                )
            else:
                await message.delete()

def setup(bot):
    bot.add_cog(LastLetterGame(bot))