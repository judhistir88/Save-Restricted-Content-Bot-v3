# Copyright (c) 2025 devgagan : https://github.com/devgaganin.
# Licensed under the GNU General Public License v3.0.
# See LICENSE file in the repository root for full license text.

import asyncio
import importlib
import os
import sys
import threading
from shared_client import start_client, app as bot_app
import app as web_app  # Import the web server module
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Track the last activity time
LAST_ACTIVITY_TIME = None
WARNING_MESSAGE = None
SLEEP_MESSAGE = None

# Check if the wake_me_up environment variable is set to true
WAKE_ME_UP = os.getenv("WAKE_ME_UP", "false").lower() == "true"
WAKE_ME_UP_URL = os.getenv("WAKE_ME_UP_URL", "")

async def load_and_run_plugins():
    await start_client()
    bot_username = (await bot_app.get_me()).username
    print(f"Deployment Connected to @{bot_username}")
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()

async def bot_main():
    global LAST_ACTIVITY_TIME, bot_owner_id
    await load_and_run_plugins()
    LAST_ACTIVITY_TIME = asyncio.get_event_loop().time()
    bot_owner_id = (await bot_app.get_me()).id
    while True:
        await asyncio.sleep(1)
        if WAKE_ME_UP:
            # Check for inactivity
            current_time = asyncio.get_event_loop().time()
            if current_time - LAST_ACTIVITY_TIME > 29 * 60:
                await send_warning_message()
                await asyncio.sleep(50)
                await send_sleeping_message()

async def send_warning_message():
    global WARNING_MESSAGE
    if WARNING_MESSAGE is None:
        WARNING_MESSAGE = await bot_app.send_message(
            chat_id=bot_owner_id,  # Send to bot owner ID
            text="Bot will sleep in 1 minute."
        )

async def send_sleeping_message():
    global WARNING_MESSAGE, SLEEP_MESSAGE
    if WARNING_MESSAGE is not None:
        await WARNING_MESSAGE.delete()
        WARNING_MESSAGE = None
    if SLEEP_MESSAGE is None:
        button = InlineKeyboardButton("Wake Me Up", url=WAKE_ME_UP_URL)
        markup = InlineKeyboardMarkup([[button]])
        SLEEP_MESSAGE = await bot_app.send_message(
            chat_id=bot_owner_id,  # Send to bot owner ID
            text="Bot is sleeping.",
            reply_markup=markup
        )

@bot_app.on_message(filters.all)
async def handle_message(client, message):
    global LAST_ACTIVITY_TIME, SLEEP_MESSAGE
    LAST_ACTIVITY_TIME = asyncio.get_event_loop().time()
    if SLEEP_MESSAGE is not None:
        await asyncio.sleep(5)
        await SLEEP_MESSAGE.delete()
        SLEEP_MESSAGE = None

def run_web_server():
    port = int(os.environ.get("PORT", 5000))
    web_app.app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print("Starting clients ...")
    try:
        bot_thread = threading.Thread(target=lambda: loop.run_until_complete(bot_main()))
        web_server_thread = threading.Thread(target=run_web_server)
        bot_thread.start()
        web_server_thread.start()
        bot_thread.join()
        web_server_thread.join()
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        sys.exit(1)
    finally:
        try:
            loop.close()
        except Exception:
            pass
