import asyncio
import discord
from discord import app_commands

# Role allowed to stop the bot (as integer)
ALLOWED_ROLE_ID = 1446136633538777099

def register(tree: app_commands.CommandTree):
    @tree.command(name='shutdown', description='Shut down the bot (role-restricted)')
    async def shutdown(interaction: discord.Interaction):
        # Must be invoked in a guild and the user must have the allowed role
        if interaction.guild is None:
            await interaction.response.send_message('This command must be used in a server channel.', ephemeral=True)
            return

        member = interaction.user
        # Ensure we have a Member object
        if not isinstance(member, discord.Member):
            # Try fetching member
            try:
                member = await interaction.guild.fetch_member(interaction.user.id)
            except Exception:
                await interaction.response.send_message('Could not verify your roles.', ephemeral=True)
                return

        has_role = any(r.id == ALLOWED_ROLE_ID for r in member.roles)
        if not has_role:
            await interaction.response.send_message('You do not have permission to stop the bot.', ephemeral=True)
            return

        # Authorized — acknowledge and shut down
        await interaction.response.send_message('Shutting down... (authorized)', ephemeral=True)
        # small delay so user sees response
        print(f'Shutdown command received from authorized user: {interaction.user} ({interaction.user.id})')
        await asyncio.sleep(0.4)
        await interaction.client.close()
