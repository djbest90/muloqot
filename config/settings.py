from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(admin_id) for admin_id in os.getenv("ADMIN_IDS").split(",")]
DB_PATH = os.getenv("DB_PATH")
BASE_URL = os.getenv('BASE_URL')
BACK_USERNAME = os.getenv('BACK_USERNAME')
BACK_PASSWORD = os.getenv('BACK_PASSWORD')