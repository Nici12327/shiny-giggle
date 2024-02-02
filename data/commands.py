#import discord
#from discord import app_commands

#intents = discord.Intents.default()

#client = discord.Client(intents=intents)
#tree = app_commands.CommandTree(client)

#class startup:
#    print('commands.py is loaded')

#class cmds:
#    @tree.command(
#    name='ping',
#    description='Check if bot is online/running correctly',
#    guild=discord.Object(id=963791704492748870)
#    )
#    async def ping(interaction):
#        await interaction.response.send_message('Pong')