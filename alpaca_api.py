import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()

API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = os.getenv("APCA_API_BASE_URL")

# Connect to Alpaca
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

def get_account():
    """Returns account info"""
    return api.get_account()

def place_buy_order(symbol, usd_amount):
    """Places a fractional market buy order for given USD amount"""
    api.submit_order(
        symbol=symbol,
        notional=usd_amount,
        side='buy',
        type='market',
        time_in_force='day'
    )

def place_sell_order(symbol):
    """
    Sells the entire current position for the symbol (fractional or full).
    """
    try:
        position = api.get_position(symbol)
        qty = float(position.qty)
        qty_available = float(position.qty_available)

        if qty_available > 0:
            print(f"[SELL] Selling {qty_available} of {symbol} at market price")
            api.submit_order(
                symbol=symbol,
                qty=qty_available,
                side='sell',
                type='market',
                time_in_force='day'
            )
        else:
            print(f"No available quantity to sell for {symbol}. Skipping order.")

    except tradeapi.rest.APIError as e:
        if "position does not exist" in str(e).lower():
            print(f"No position exists for {symbol}. Nothing to sell.")
        else:
            raise



def get_current_price(symbol):
    """Fetches the latest trade price for the given symbol"""
    quote = api.get_latest_trade(symbol)
    return quote.price
