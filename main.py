import discord
from discord import app_commands

from data.token import token

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("----------")
    print("Bot is up!")
    print("----------")
    print(" ")

@tree.command(
    name='ping',
    description='Check if bot is online/running correctly',
    guild=discord.Object(id=963791704492748870)
)
async def ping(interaction):
    await interaction.response.send_message('Pong')

@tree.command(
    name='hi',
    description='Say hi to the Bot'
)
async def hi(ctx):
    await ctx.send_message('Hey!')

client.run(token)