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

# SUSTITUYE ESTO por la ID de tu canal de bienvenidas (en Discord: clic derecho en el canal > Copiar ID del canal)
ID_CANAL_BIENVENIDA = 1557394035398676593

# Enlace de imagen/GIF para la despedida
URL_IMAGEN_DESPEDIDA = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHI4Y2dtZ2RkZXhhZ2s0eXp2aThzcDZwb3RzbzJ4eTl6ZjJxd3p4OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/L952342342/giphy.gif"

@client.event
async def on_ready():
    print(f'Culón Bot está en línea como {client.user}')

@client.event
async def on_member_join(member):
    canal = client.get_channel(ID_CANAL_BIENVENIDA)
    if canal:
        await canal.send(f'¡Buenas {member.mention}! Bienvenido/a a **C.U.L.O.S.** 🍑 Pásate por el canal de normas para verificarte.')

@client.event
async def on_member_remove(member):
    canal = client.get_channel(ID_CANAL_BIENVENIDA)
    if canal:
        await canal.send(
            f'**{member.mention}** (`{member.name}`) se ha ido del servidor... Una lástima. 👋\n{URL_IMAGEN_DESPEDIDA}'
        )

keep_alive()
token = os.environ.get('DISCORD_TOKEN')
client.run(token)
