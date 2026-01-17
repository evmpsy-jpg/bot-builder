import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# API
API_URL = 'http://localhost:8000/api'

# Database
DB_PATH = 'bot_users.db'

# Bot ID в системе flows
BOT_ID = 1
