import discord
from discord.ext import commands
from discord.ui import Select, View
import os
import json
import random
import time
import datetime
from flask import Flask
from threading import Thread

# --- Servidor web para mantenerlo vivo en Render ---
app = Flask('')

@app.route('/')
def home():
    return "¡Culón Bot está vivo!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- Configuración del Bot ---
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs DE LOS CANALES
ID_CANAL_BIENVENIDA = 1557394035398676593
ID_CANAL_DESPEDIDA = 1557394275556261990
ID_CANAL_NIVELES = 1558453005571858453       # Canal 🆙 | NIVELES
ID_CANAL_CONFESIONES = 1558457338233618513   # Canal #confesiones
ID_CANAL_SUGERENCIAS = 1558457514981462106   # Canal #sugerencias

# Enlaces de las imágenes / GIFs
URL_FOTO_BIENVENIDA = "https://cdn.discordapp.com/attachments/1557496548336869428/1557511850462158970/Banner_de_perfil_para_Discord_arte_pixelado_magenta_violeta.png?backend=b2&ex=6ac8ba32&is=6ac768b2&hm=cd90bce37fae41083068b8718b019fe080b8861d54ea289a008e215dd37eb56f&"
URL_FOTO_DESPEDIDA = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDcxczczbHQ2cXVjaGhmcml2b29raXd6d3d3YWRqYmsydWJ4NHh4YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/GWir0luSQnBpbbvqwM/giphy.gif"

# --- Base de datos local de Niveles (JSON) ---
LEVELS_FILE = "niveles.json"
user_cooldowns = {}

def cargar_niveles():
    if os.path.exists(LEVELS_FILE):
        with open(LEVELS_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_niveles(data):
    with open(LEVELS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Menú Desplegable de Autorroles (Juegos) ---
class SelectJuegos(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="𝐕𝐀𝐋𝐎𝐑𝐀𝐍𝐓", emoji="🔫", description="Rol de VALORANT"),
            discord.SelectOption(label="𝐅𝐎𝐑𝐓𝐍𝐈𝐓𝐄", emoji="💥", description="Rol de FORTNITE"),
            discord.SelectOption(label="𝐀𝐌𝐎𝐍𝐆 𝐔𝐒", emoji="🔪", description="Rol de AMONG US"),
            discord.SelectOption(label="𝐑𝐎𝐁𝐋𝐎𝐗", emoji="🧱", description="Rol de ROBLOX"),
            discord.SelectOption(label="𝐏𝐎𝐊𝐄𝐌𝐎𝐍", emoji="⚡", description="Rol de POKEMON"),
            discord.SelectOption(label="𝐆𝐀𝐑𝐓𝐈𝐂 𝐏𝐇𝐎𝐍𝐄", emoji="📱", description="Rol de GARTIC PHONE"),
            discord.SelectOption(label="𝐑OСКEТ", emoji="🚗", description="Rol de ROCKET"),
            discord.SelectOption(label="𝐁𝐑𝐀𝐖𝐋", emoji="🥊", description="Rol de BRAWL STARS"),
        ]
        super().__init__(placeholder="Elige tus juegos aquí...", min_values=0, max_values=len(options), options=options)

    async def callback(self, interaction: discord.Interaction):
        roles_dict = {
            "𝐕𝐀𝐋𝐎𝐑𝐀𝐍𝐓": "𝐕𝐀𝐋𝐎𝐑𝐀𝐍𝐓",
            "𝐅𝐎𝐑𝐓𝐍𝐈𝐓𝐄": "𝐅𝐎𝐑𝐓NITE",
            "𝐀𝐌𝐎𝐍𝐆 𝐔𝐒": "𝐀𝐌𝐎𝐍𝐆 𝐔𝐒",
            "𝐑𝐎𝐁𝐋𝐎𝐗": "𝐑𝐎𝐁𝐋𝐎𝐗",
            "𝐏𝐎𝐊𝐄𝐌𝐎𝐍": "𝐏𝐎𝐊𝐄𝐌𝐎𝐍",
            "𝐆𝐀𝐑𝐓𝐈𝐂 𝐏𝐇𝐎𝐍𝐄": "𝐆𝐀𝐑𝐓𝐈𝐂 𝐏𝐇𝐎𝐍𝐄",
            "𝐑𝐎𝐂𝐊𝐄𝐓": "𝐑𝐎𝐂𝐊𝐄𝐓",
            "𝐁𝐑𝐀𝐖𝐋": "𝐁𝐑𝐀𝐖𝐋"
        }

        guild = interaction.guild
        member = interaction.user
        respuestas = []

        for label, role_name in roles_dict.items():
            rol = discord.utils.get(guild.roles, name=role_name)
            if rol:
                if label in self.values:
                    if rol not in member.roles:
                        await member.add_roles(rol)
                        respuestas.append(f"✅ Añadido: **{role_name}**")
                else:
                    if rol in member.roles:
                        await member.remove_roles(rol)
                        respuestas.append(f"❌ Quitado: **{role_name}**")

        if not respuestas:
            await interaction.response.send_message("No has realizado cambios en tus roles.", ephemeral=True)
        else:
            await interaction.response.send_message("\n".join(respuestas), ephemeral=True)

class RolesView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectJuegos())


# --- Sistema de Colores por Botones ---
ROLES_COLORES = [
    "Rojo", "Azul", "Verde", "Rosa", 
    "Amarillo", "Morado", "Naranja", "Cian", 
    "Negro", "Blanco", "Marrón", "Gris"
]

class ColorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def cambiar_color(self, interaction: discord.Interaction, nombre_rol: str):
        guild = interaction.guild
        member = interaction.user

        roles_a_quitar = [r for r in member.roles if r.name in ROLES_COLORES]
        if roles_a_quitar:
            await member.remove_roles(*roles_a_quitar)

        rol_nuevo = discord.utils.get(guild.roles, name=nombre_rol)
        if rol_nuevo:
            await member.add_roles(rol_nuevo)
            await interaction.response.send_message(f"🎨 Te has puesto el color **{nombre_rol}**.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ El rol `{nombre_rol}` no existe en el servidor.", ephemeral=True)

    # --- Fila 1 ---
    @discord.ui.button(label="Rojo", style=discord.ButtonStyle.danger, custom_id="btn_rojo", row=0)
    async def btn_rojo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Rojo")

    @discord.ui.button(label="Azul", style=discord.ButtonStyle.primary, custom_id="btn_azul", row=0)
    async def btn_azul(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Azul")

    @discord.ui.button(label="Verde", style=discord.ButtonStyle.success, custom_id="btn_verde", row=0)
    async def btn_verde(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Verde")

    @discord.ui.button(label="Rosa", style=discord.ButtonStyle.secondary, custom_id="btn_rosa", row=0)
    async def btn_rosa(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Rosa")

    # --- Fila 2 ---
    @discord.ui.button(label="Amarillo", style=discord.ButtonStyle.secondary, custom_id="btn_amarillo", row=1)
    async def btn_amarillo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Amarillo")

    @discord.ui.button(label="Morado", style=discord.ButtonStyle.secondary, custom_id="btn_morado", row=1)
    async def btn_morado(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Morado")

    @discord.ui.button(label="Naranja", style=discord.ButtonStyle.secondary, custom_id="btn_naranja", row=1)
    async def btn_naranja(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Naranja")

    @discord.ui.button(label="Cian", style=discord.ButtonStyle.secondary, custom_id="btn_cian", row=1)
    async def btn_cian(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Cian")

    # --- Fila 3 ---
    @discord.ui.button(label="Negro", style=discord.ButtonStyle.secondary, custom_id="btn_negro", row=2)
    async def btn_negro(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Negro")

    @discord.ui.button(label="Blanco", style=discord.ButtonStyle.secondary, custom_id="btn_blanco", row=2)
    async def btn_blanco(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Blanco")

    @discord.ui.button(label="Marrón", style=discord.ButtonStyle.secondary, custom_id="btn_marron", row=2)
    async def btn_marron(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Marrón")

    @discord.ui.button(label="Gris", style=discord.ButtonStyle.secondary, custom_id="btn_gris", row=2)
    async def btn_gris(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cambiar_color(interaction, "Gris")


# --- Eventos del Bot ---
@bot.event
async def on_ready():
    print(f'Culón Bot está en línea como {bot.user}')

@bot.event
async def on_member_join(member):
    canal = bot.get_channel(ID_CANAL_BIENVENIDA)
    if canal:
        embed = discord.Embed(
            description=f'¡Buenas {member.mention}! Bienvenido/a a **C.U.L.O.S.** 🍑 Pásate por el canal de normas para verificarte.',
            color=0xff00ff
        )
        embed.set_image(url=URL_FOTO_BIENVENIDA)
        await canal.send(embed=embed)

@bot.event
async def on_member_remove(member):
    canal = bot.get_channel(ID_CANAL_DESPEDIDA)
    if canal:
        embed = discord.Embed(
            description=f'**{member.mention}** (`{member.name}`) ha sufrido combustión espontánea y ya no está en el servidor. 🔥💥',
            color=0xff4500
        )
        embed.set_image(url=URL_FOTO_DESPEDIDA)
        await canal.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Ganancia de XP al chatear
    user_id = str(message.author.id)
    current_time = time.time()

    if user_id not in user_cooldowns or current_time - user_cooldowns
