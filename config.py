import os
from dotenv import load_dotenv

load_dotenv()

# API Credentials
OLYMPTRADE_EMAIL = os.getenv("OLYMPTRADE_EMAIL")
OLYMPTRADE_PASSWORD = os.getenv("OLYMPTRADE_PASSWORD")
OLYMPTRADE_ACCESS_TOKEN = os.getenv("OLYMPTRADE_ACCESS_TOKEN")

# Trading Parameters
TRADING_PAIR = os.getenv("TRADING_PAIR", "LATAM_X")
TRADE_AMOUNT = int(os.getenv("TRADE_AMOUNT", "1"))
TRADE_DURATION = int(os.getenv("TRADE_DURATION", "60"))  # seconds
ACCOUNT_GROUP = os.getenv("ACCOUNT_GROUP", "demo")

# Bot Settings
MAX_OPEN_TRADES = 5
STOP_LOSS_PERCENT = 10
TAKE_PROFIT_PERCENT = 20