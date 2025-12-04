import discord
from discord import app_commands

def register(tree: app_commands.CommandTree):
    @tree.command(name='clear', description='Clear recent messages in this channel')
    @app_commands.describe(limit='Number of messages to delete (default 50)')
    async def clear_cmd(interaction: discord.Interaction, limit: int = 50):
        # Ensure we have a TextChannel
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message('This command must be used in a text channel.', ephemeral=True)
            return

        # Defer response (could take time)
        await interaction.response.defer(ephemeral=True)

        try:
            # purge requires appropriate permissions; limit must be positive
            limit = max(1, min(limit, 1000))
            deleted = await channel.purge(limit=limit)
            await interaction.followup.send(f'Cleared {len(deleted)} messages.')
        except discord.Forbidden:
            await interaction.followup.send('I do not have permission to delete messages here.')
        except Exception as e:
            await interaction.followup.send(f'Failed to clear messages: {e}')
