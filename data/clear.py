import asyncio
import discord
from discord import app_commands


async def _purge_in_batches(channel: discord.TextChannel, total: int) -> int:
    """Purge messages in batches until `total` messages are deleted or no more deletable messages remain.

    Returns the number of messages actually deleted.
    """
    deleted_total = 0
    remaining = max(1, min(total, 1000))

    while remaining > 0:
        batch = min(100, remaining)
        # channel.purge returns list of deleted messages
        deleted = await channel.purge(limit=batch)
        if not deleted:
            # nothing deleted in this batch -> stop
            break
        deleted_total += len(deleted)
        remaining -= len(deleted)
        # small pause to avoid hitting rate limits
        await asyncio.sleep(0.2)

    return deleted_total


async def _delete_individually(channel: discord.TextChannel, total: int) -> int:
    """Delete messages one-by-one until `total` messages are deleted or no more messages.

    This is a fallback used when bulk purge cannot remove messages (for example
    messages older than 14 days). It is slower and respects a small delay to
    reduce rate-limit pressure.
    """
    deleted = 0
    # We iterate over history and attempt per-message deletion
    async for message in channel.history(limit=min(1000, total * 3)):
        if deleted >= total:
            break
        try:
            await message.delete()
            deleted += 1
            await asyncio.sleep(0.25)  # small pause between deletes
        except discord.Forbidden:
            # cannot delete this message; skip it
            continue
        except Exception:
            # skip problematic message and continue
            continue

    return deleted


def register(tree: app_commands.CommandTree):
    @tree.command(name='clear', description='Clear recent messages in this channel')
    @app_commands.describe(limit='Number of messages to delete (default 20)')
    async def clear_cmd(interaction: discord.Interaction, limit: int = 20):
        # Ensure we have a TextChannel
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message('This command must be used in a text channel.', ephemeral=True)
            return

        # Defer response (could take time)
        await interaction.response.defer(ephemeral=True)

        try:
            deleted = await _purge_in_batches(channel, limit)

            # If we couldn't delete enough via bulk purge, attempt per-message fallback
            if deleted < limit:
                remaining = limit - deleted
                fallback_deleted = await _delete_individually(channel, remaining)
                deleted += fallback_deleted

            await interaction.followup.send(f'Cleared {deleted} messages.')
        except discord.Forbidden:
            await interaction.followup.send('I do not have permission to delete messages here.')
        except Exception as e:
            await interaction.followup.send(f'Failed to clear messages: {e}')
