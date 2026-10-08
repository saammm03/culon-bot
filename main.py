import discord
import os
from flask import Flask
from threading import Thread

# --- Servidor web para mantenerlo vivo en Render ---
app = Flask('')

@app.route('/')
def home():
    return "¡Culón Bot está vivo!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- Configuración del Bot ---
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# IDs DE LOS CANALES
ID_CANAL_BIENVENIDA = 1557394035398676593
ID_CANAL_DESPEDIDA = 1557394275556261990

# Enlaces de las imágenes / GIFs
URL_FOTO_BIENVENIDA = "https://cdn.discordapp.com/attachments/1557496548336869428/1557511850462158970/Banner_de_perfil_para_Discord_arte_pixelado_magenta_violeta.png?backend=b2&ex=6ac8ba32&is=6ac768b2&hm=cd90bce37fae41083068b8718b019fe080b8861d54ea289a008e215dd37eb56f&"
URL_FOTO_DESPEDIDA = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDcxczczbHQ2cXVjaGhmcml2b29raXd6d3d3YWRqYmsydWJ4NHh4YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/GWir0luSQnBpbbvqwM/giphy.gif"

@client.event
async def on_ready():
    print(f'Culón Bot está en línea como {client.user}')

@client.event
async def on_member_join(member):
    canal = client.get_channel(ID_CANAL_BIENVENIDA)
    if canal:
        embed = discord.Embed(
            description=f'¡Buenas {member.mention}! Bienvenido/a a **C.U.L.O.S.** 🍑 Pásate por el canal de normas para verificarte.',
            color=0xff00ff # Color magenta
        )
        embed.set_image(url=URL_FOTO_BIENVENIDA)
        await canal.send(embed=embed)

@client.event
async def on_member_remove(member):
    canal = client.get_channel(ID_CANAL_DESPEDIDA)
    if canal:
        embed = discord.Embed(
            description=f'**{member.mention}** (`{member.name}`) ha sufrido combustión espontánea y ya no está en el servidor. 🔥💥',
            color=0xff4500 # Color naranja/fuego
        )
        embed.set_image(url=URL_FOTO_DESPEDIDA)
        await canal.send(embed=embed)

keep_alive()
token = os.environ.get('DISCORD_TOKEN')
client.run(token)

keep_alive()
token = os.environ.get('DISCORD_TOKEN')
client.run(token)
