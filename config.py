# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import os
from dotenv import load_dotenv

load_dotenv()

# VPS --- FILL COOKIES 🍪 in """ ... """

INST_COOKIES = """
# write up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_DB = os.getenv("MONGO_DB", "")
OWNER_ID = list(map(int, os.getenv("OWNER_ID", "").split()))  # list separated via space
DB_NAME = os.getenv("DB_NAME", "telegram_downloader")
STRING = os.getenv("STRING", None)  # optional
LOG_GROUP = int(os.getenv("LOG_GROUP", "-1001234456"))  # optional with -100
FORCE_SUB = int(os.getenv("FORCE_SUB", "-10012345567"))  # optional with -100
MASTER_KEY = os.getenv("MASTER_KEY", "gK8HzLfT9QpViJcYeB5wRa3DmN7P2xUq")  # for session encryption
IV_KEY = os.getenv("IV_KEY", "s7Yx5CpVmE3F")  # for decryption
YT_COOKIES = os.getenv("YT_COOKIES", YTUB_COOKIES)
INSTA_COOKIES = os.getenv("INSTA_COOKIES", INST_COOKIES)
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT = int(os.getenv("PREMIUM_LIMIT", "500"))

# New environment variables from main.py
WAKE_ME_UP = os.getenv("WAKE_ME_UP", "false").lower() == "true" # set to true, for pinning wake me up url
WAKE_ME_UP_URL = os.getenv("WAKE_ME_UP_URL", " ") # Get from Web service under services "https://immense-elsa-dhyty-aeff.koyeb.app/". 
MAX_PIN_COUNT = int(os.getenv("MAX_PIN_COUNT", "2"))  # wake up bot for 29 minutes if value set to 1 for bot deployed on koyeb.
PORT = int(os.environ.get("PORT", 5000))  # default to 5000 if not set
