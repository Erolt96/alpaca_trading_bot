import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone


load_dotenv()

API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = os.getenv("APCA_API_BASE_URL")

# initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')


def get_price_change_percent(symbol="TSLA", minutes=120):
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)

    start_str = start.isoformat().replace("+00:00", "Z")
    end_str = end.isoformat().replace("+00:00", "Z")

    barset = api.get_bars(
        symbol,
        timeframe="1Min",
        start=start_str,
        end=end_str,
        feed='iex'
    )

    bars = list(barset)

    if len(bars) < 2:
        print("Not enough data to calculate price change.")
        return None

    old_price = bars[0].c
    new_price = bars[-1].c

    print(f"Old price (2h ago): {old_price}, New price (now): {new_price}")
    print(f"Bars returned: {len(bars)}")

    percent_change = ((new_price - old_price) / old_price) * 100
    return percent_change


def should_buy():
    change = get_price_change_percent()
    if change is None:
        return False
    print(f"[Signal Check] TSLA price change = {change:.2f}%")
    return change >= 0.2  # if it moves by 0.2% in last 2 hours then it buys
