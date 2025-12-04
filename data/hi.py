import discord
from discord import app_commands

def register(tree: app_commands.CommandTree):
    @tree.command(name='hi', description='Say hi to the Bot')
    async def hi(interaction: discord.Interaction):
        await interaction.response.send_message('Hey!')
