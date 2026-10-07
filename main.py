import discord
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Culón Bot está en línea como {client.user}')

token = os.environ.get('DISCORD_TOKEN')
client.run(token)
