# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import os
import asyncio
from shared_client import start_client
import importlib
import aiohttp

async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()

async def fetch_random_fun_fact():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://uselessfacts.jsph.pl/random.json?language=en') as response:
            if response.status == 200:
                data = await response.json()
                return data['text']
            else:
                return "Could not fetch a fun fact at this time."

async def send_random_message(bot_owner, count, interval):
    for _ in range(count):
        fun_fact = await fetch_random_fun_fact()
        # Replace the following line with actual code to send message via bot
        print(f"Sending fun fact to {bot_owner}: {fun_fact}")
        await asyncio.sleep(interval * 60)  # Sleep for interval minutes

async def wake_me_up_schedule():
    WAKE_ME_UP = os.getenv('WAKE_ME_UP', 'false').lower() == 'true'
    RANDOM_MESSAGE_COUNT = int(os.getenv('RANDOM_MESSAGE_COUNT', '3'))
    BOT_OWNER = os.getenv('BOT_OWNER', 'your_default_bot_owner_id')
    MESSAGE_INTERVAL = int(os.getenv('MESSAGE_INTERVAL', '29'))  # Get interval from env

    if WAKE_ME_UP:
        await send_random_message(BOT_OWNER, RANDOM_MESSAGE_COUNT, MESSAGE_INTERVAL)

async def main():
    await load_and_run_plugins()
    await wake_me_up_schedule()
    while True:
        await asyncio.sleep(1)  # Keep the bot running

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print("Starting clients ...")
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        sys.exit(1)
    finally:
        try:
            loop.close()
        except Exception:
            pass
