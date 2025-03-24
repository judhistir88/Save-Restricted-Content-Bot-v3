from pyrogram import Client, filters
import asyncio
import os
import sys
from config import OWNER_ID  # Ensure OWNER_ID is defined in your config

app = Client("my_bot")

@app.on_message(filters.command("reboot") & filters.user(OWNER_ID))
async def reboot_command(client, message):
    rebooting_message = await message.reply_text("Rebooting the bot...")
    await client.send_message(chat_id=OWNER_ID, text="Bot is rebooting...")
    os.execl(sys.executable, sys.executable, *sys.argv)

@app.on_message(filters.private & filters.user(OWNER_ID))
async def notify_reboot_success(client, message):
    if message.text == "/reboot":
        success_message = await client.send_message(chat_id=OWNER_ID, text="Bot has successfully rebooted.")
        
        # Add a callback to delete the messages after 10 seconds
        await asyncio.sleep(10)
        await success_message.delete()
        await message.delete()

# Note: Ensure that the OWNER_ID constant is defined somewhere in your config or main script.
