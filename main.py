import discord
from discord import app_commands
import os
import shutil

from data.credentials import token
from data import register_all, ai_responder

# Delete all conversation logs on startup
log_dir = "data/conversation_logs"
if os.path.exists(log_dir):
    try:
        shutil.rmtree(log_dir)
        print("Cleared all conversation logs")
    except Exception as e:
        print(f"Could not delete conversation logs: {e}")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    # Print all guilds the bot is in
    print(' ')
    print('Bot Servers:')
    for g in client.guilds:
        print(f'{g.name} (id={g.id})')
        print(' ')

    # Register commands (modules under data/) and initialize event listeners
    try:
        register_all(tree, client)
        await ai_responder.setup(client)
        synced = await tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to register/sync commands: {e}')


client.run(token)
