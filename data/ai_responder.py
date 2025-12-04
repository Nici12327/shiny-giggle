import asyncio
import requests
import discord

# Configuration
TARGET_CHANNEL_ID = 1446140885199749290
OLLAMA_BASE = "http://192.168.178.20:11434"
MODEL = "gemma3:270m"
REQUEST_TIMEOUT = 15


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

    # indicate typing while we call Ollama
    try:
        async with message.channel.typing():
            # run blocking request in threadpool
            loop = asyncio.get_running_loop()
            try:
                response_text = await loop.run_in_executor(None, _call_ollama, prompt)
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

    async def on_message(message: discord.Message):
        await _handle_message(message)

    client.add_listener(on_message)
