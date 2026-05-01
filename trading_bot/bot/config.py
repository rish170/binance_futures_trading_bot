import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "")
API_SECRET = os.getenv("API_SECRET", "")
BASE_URL = os.getenv("BASE_URL", "https://testnet.binancefuture.com")

if not API_KEY or not API_SECRET:
    print("WARNING: API_KEY or API_SECRET not set in environment.")
