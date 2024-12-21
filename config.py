import os
from dotenv import load_dotenv

load_dotenv()

MAX_THREADS = 5
DROPBOX_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
