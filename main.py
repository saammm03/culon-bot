import discord
from discord.ext import commands
from discord.ui import Select, View
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
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs DE LOS CANALES
ID_CANAL_BIENVENIDA = 1557394035398676593
ID_CANAL_DESPEDIDA = 1557394275556261990

# Enlaces de las imágenes / GIFs
URL_FOTO_BIENVENIDA = "https://cdn.discordapp.com/attachments/1557496548336869428/1557511850462158970/Banner_de_perfil_para_Discord_arte_pixelado_magenta_violeta.png?backend=b2&ex=6ac8ba32&is=6ac768b2&hm=cd90bce37fae41083068b8718b019fe080b8861d54ea289a008e215dd37eb56f&"
URL_FOTO_DESPEDIDA = "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaDcxczczbHQ2cXVjaGhmcml2b29raXd6d3d3YWRqYmsydWJ4NHh4YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/GWir0luSQnBpbbvqwM/giphy.gif"

# --- Menú Desplegable de Autorroles ---
class SelectJuegos(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="𝐕𝐀𝐋𝐎𝐑𝐀𝐍𝐓", emoji="🔫", description="Rol de VALORANT"),
            discord.SelectOption(label="𝐅𝐎𝐑𝐓𝐍𝐈𝐓𝐄", emoji="💥", description="Rol de FORTNITE"),
            discord.SelectOption(label="𝐀𝐌𝐎𝐍𝐆 𝐔𝐒", emoji="🔪", description="Rol de AMONG US"),
            discord.SelectOption(label="𝐑𝐎𝐁𝐋𝐎𝐗", emoji="🧱", description="Rol de ROBLOX"),
            discord.SelectOption(label="𝐏𝐎𝐊𝐄𝐌𝐎𝐍", emoji="⚡", description="Rol de POKEMON"),
            discord.SelectOption(label="𝐆𝐀𝐑𝐓𝐈𝐂 𝐏𝐇𝐎𝐍𝐄", emoji="📱", description="Rol de GARTIC PHONE"),
            discord.SelectOption(label="𝐑𝐎𝐂𝐊𝐄𝐓", emoji="🚗", description="Rol de ROCKET"),
            discord.SelectOption(label="𝐁𝐑𝐀𝐖𝐋", emoji="🥊", description="Rol de BRAWL STARS"),
        ]
        super().__init__(placeholder="Elige tus juegos aquí...", min_values=0, max_values=len(options), options=options)

    async def callback(self, interaction: discord.Interaction):
        roles_dict = {
            "𝐕𝐀𝐋𝐎𝐑𝐀𝐍𝐓": "𝐕𝐀𝐋𝐎𝐑𝐀𝐍𝐓",
            "𝐅𝐎𝐑𝐓𝐍𝐈𝐓𝐄": "𝐅𝐎𝐑𝐓𝐍𝐈𝐓𝐄",
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

# --- Comando para sacar el panel de autorroles ---
@bot.command()
@commands.has_permissions(administrator=True)
async def roles(ctx):
    embed = discord.Embed(
        title="🎮 Roles de Juegos",
        description="Selecciona en el menú desplegable los juegos a los que juegas para asignarte el rol correspondiente.",
        color=0x3498db
    )
    await ctx.send(embed=embed, view=RolesView())

keep_alive()
token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
