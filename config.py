import os
from dotenv import load_dotenv

load_dotenv()

# Original Bot Configuration
# تكوين البوت الأصلي

# Bot Token
BOT_TOKEN = "8059528086:AAFIZLlNJzo_nUplHlXzjyShla-DsT0RNYw"

# API Credentials (Get from https://my.telegram.org/auth)
API_ID = 123456  # Replace with your API ID
API_HASH = "your_api_hash_here"  # Replace with your API Hash

# Bot Username
BOT_USERNAME = "Facemedobookbot"

# Admin ID
ADMIN_ID = 5509130673

# Bot Settings
BOT_NAME = "PowerBot"
BOT_VERSION = "2.0"
BOT_DESCRIPTION = "قوي جدا - Powerful Telegram Bot"

# Database Settings (if needed)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot_database.db")

# API Keys (add your own keys here)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
TRANSLATE_API_KEY = os.getenv("TRANSLATE_API_KEY", "")

# Bot Features
ENABLED_FEATURES = [
    "admin_commands",
    "user_commands", 
    "file_handling",
    "media_processing",
    "web_scraping",
    "utilities",
    "entertainment"
]