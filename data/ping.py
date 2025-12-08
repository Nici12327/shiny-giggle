import discord
from discord import app_commands

def register(tree: app_commands.CommandTree):
    @tree.command(name='ping', description='Check if bot is online/running correctly')
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message('Pong')
        print(f'Ping command used')
