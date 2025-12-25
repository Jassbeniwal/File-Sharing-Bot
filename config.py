#(©)CodeXBotz
import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "25331263"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "cab85305bf85125a2ac053210bcd1030")

# Your db channel Id (should be negative for channels)
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1003508451850"))

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "1955406483"))

# Port for web server
PORT = int(os.environ.get("PORT", "8080"))

# Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://ultroidxTeam:ultroidxTeam@cluster0.gabxs6m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "filesharexbot")

# Force sub channel id, set to 0 or empty to disable
FORCE_SUB_CHANNEL = os.environ.get("FORCE_SUB_CHANNEL", "0")
if FORCE_SUB_CHANNEL and FORCE_SUB_CHANNEL != "0":
    FORCE_SUB_CHANNEL = int(FORCE_SUB_CHANNEL)
else:
    FORCE_SUB_CHANNEL = None

# Channel for join requests (separate from force sub)
JOIN_REQUEST_CHANNEL = os.environ.get("JOIN_REQUEST_CHANNEL", "-1002888391802")
if JOIN_REQUEST_CHANNEL:
    JOIN_REQUEST_CHANNEL = int(JOIN_REQUEST_CHANNEL)
else:
    JOIN_REQUEST_CHANNEL = None

# Bot workers
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Start message
START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/Rkv9B2Mg/1955406483-23289.jpg")
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")

# Admins list
ADMINS = []
admins_str = os.environ.get("ADMINS", "7686808821")
if admins_str:
    try:
        ADMINS = [int(x.strip()) for x in admins_str.split()]
    except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

# Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

# Set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)
if CUSTOM_CAPTION == "None":
    CUSTOM_CAPTION = None

# Set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = os.environ.get('PROTECT_CONTENT', "False").lower() == "true"

# Auto delete time in seconds (0 to disable)
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "0"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "This file will be automatically deleted in {time} seconds. Please ensure you have saved any necessary content before this time.")
AUTO_DEL_SUCCESS_MSG = os.environ.get("AUTO_DEL_SUCCESS_MSG", "Your file has been successfully deleted. Thank you for using our service. ✅")

# Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False").lower() == "true"

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

# Add owner to admins if not already present
if OWNER_ID not in ADMINS:
    ADMINS.append(OWNER_ID)

LOG_FILE_NAME = "filesharingbot.txt"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Create logger function
def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
