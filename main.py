from utils.imports import *
from utils.token import TOKEN

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
fuze = commands.Bot(command_prefix="/", intents=intents)

for filename in os.listdir('./events'):
    if filename.endswith('.py'):
        fuze.load_extension(f'events.{filename[:-3]}')

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        fuze.load_extension(f'commands.{filename[:-3]}')    

@fuze.event
async def on_ready():
    print(f'FuzeMC is ready')
    await fuze.change_presence(activity=nextcord.Game(name=f"IP: fuzemc.pl"))



fuze.run(TOKEN)