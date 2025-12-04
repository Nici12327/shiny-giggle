import asyncio
import requests
import discord
import os

# Configuration
TARGET_CHANNEL_ID = 1446140885199749290
OLLAMA_BASE = "http://192.168.178.20:11434"
MODEL = "gemma3:270m"
REQUEST_TIMEOUT = 15
CONVERSATION_LOGS_DIR = "data/conversation_logs"

# Ensure logs directory exists
os.makedirs(CONVERSATION_LOGS_DIR, exist_ok=True)


def _get_user_log_file(user_id: int) -> str:
    """Get the conversation log file path for a user."""
    return os.path.join(CONVERSATION_LOGS_DIR, f"user_{user_id}.txt")


def _save_conversation(user_id: int, history: list):
    """Save conversation history to a user-specific text file."""
    try:
        # Ensure logs directory exists
        os.makedirs(CONVERSATION_LOGS_DIR, exist_ok=True)
        log_file = _get_user_log_file(user_id)
        with open(log_file, 'w', encoding='utf-8') as f:
            for author_name, msg_content in history:
                if msg_content.strip():
                    f.write(f"{author_name}: {msg_content}\n")
    except Exception as e:
        print(f"Error saving conversation log for user {user_id}: {e}")


def _load_conversation(user_id: int) -> str:
    """Load conversation history from a user's log file."""
    try:
        log_file = _get_user_log_file(user_id)
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        print(f"Error loading conversation log for user {user_id}: {e}")
    return ""


def _call_ollama(prompt: str) -> str:
    """Call Ollama generate endpoint and return the response text.

    Returns the generated text or raises requests.RequestException on failure.
    """
    url = f"{OLLAMA_BASE}/api/generate"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    resp = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    # Ollama's response key may be `response` or nested; attempt to read safely
    if isinstance(data, dict):
        return data.get("response") or data.get("text") or str(data)
    return str(data)


async def _handle_message(message: discord.Message):
    # ignore bot messages
    if message.author.bot:
        return

    if message.channel.id != TARGET_CHANNEL_ID:
        return

    prompt = message.content.strip()
    if not prompt:
        return

    # Fetch conversation history (last 20 messages)
    try:
        history = []
        async for msg in message.channel.history(limit=20):
            # Only include messages from users and the bot
            if msg.author.bot or not msg.author.bot:
                history.append((msg.author.name, msg.content))
    except Exception:
        history = []

    # Reverse to get chronological order (oldest first)
    history.reverse()

    # Save conversation to user-specific file
    _save_conversation(message.author.id, history)

    # Load the full conversation history for the user
    user_history = _load_conversation(message.author.id)

    # Build full prompt with user's complete conversation history
    full_prompt = f"User {message.author.name}'s conversation history:\n{user_history}\nRespond to the latest message appropriately."

    # indicate typing while we call Ollama
    try:
        async with message.channel.typing():
            # run blocking request in threadpool
            loop = asyncio.get_running_loop()
            try:
                response_text = await loop.run_in_executor(None, _call_ollama, full_prompt)
            except Exception as e:
                await message.reply(f"Error contacting AI: {e}", mention_author=False)
                return

            if not response_text:
                await message.reply("(AI returned empty response)", mention_author=False)
                return

            # reply to the user
            await message.reply(response_text, mention_author=False)
    except Exception:
        # swallow unexpected exceptions to avoid crashing listener
        return


async def setup(client: discord.Client):
    """Register the message handler on the given client."""
    
    # Check if on_message is already registered to avoid duplicate listeners
    if not hasattr(client, '_ai_responder_registered'):
        @client.event
        async def on_message(message: discord.Message):
            await _handle_message(message)
        
        client._ai_responder_registered = True
