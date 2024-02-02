import discord
from discord import app_commands

token = "MTIwMjk1Mzk1NDA0NTA3MTQxMA.GsmN94.JbomqXRvI5j1Tw717vOeuIlTjKn3SeA5Rhk47c"

intents = discord.Intents.default()

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("----------")
    print("Bot is up!")
    print("----------")

@tree.command(
    name='ping',
    description='Check if bot is online/running correctly',
    guild=discord.Object(id=963791704492748870)
)
async def ping(interaction):
    await interaction.response.send_message('Pong')

#from data.commands import startup
#from data.commands import cmds

client.run(token)