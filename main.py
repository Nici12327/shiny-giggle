import discord
from discord import app_commands

from data.credentials import token
from data import register_all

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

start = input('Do you want to start the bot? N/Y   ')
if start.strip().upper() == 'N':
    exit()


@client.event
async def on_ready():
    print('Bot is up!')

    # Print all guilds the bot is in
    print('Bot guilds:')
    for g in client.guilds:
        print(f'{g.name} (id={g.id})')

    # Register commands (modules under data/) and initialize event listeners
    try:
        register_all(tree, client)
        synced = await tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to register/sync commands: {e}')


client.run(token)
