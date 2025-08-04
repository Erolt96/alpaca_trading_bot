from alpaca_api import get_account, place_buy_order, place_sell_order, get_current_price, api
from strategy import should_buy
from notifier import send_email_alert
from risk_manager import calculate_trade_amount
from logger import log_event
from sell_strategy import should_sell

import json
import os



# Load config
with open("config.json", "r") as f:
    config = json.load(f)

take_profit = config["take_profit"]
stop_loss = config["stop_loss"]

print(f"[CONFIG] Using TP={take_profit}, SL={stop_loss}, Alloc={config['allocation_percent']}")

ENTRY_FILE = "entry_price.json"
SYMBOL = "TSLA"

def save_entry_price(price):
    with open(ENTRY_FILE, "w") as f:
        json.dump({"entry_price": price}, f)

def load_entry_price():
    if os.path.exists(ENTRY_FILE):
        with open(ENTRY_FILE, "r") as f:
            data = json.load(f)
            return data.get("entry_price")
    return None

def main():

    account = get_account()
    print("Account Status:", account.status)
    print("Buying Power: $", account.buying_power)


    positions = api.list_positions()
    has_tsla = any(pos.symbol == SYMBOL for pos in positions)

    #clean up stale entry if no position
    if not has_tsla and os.path.exists(ENTRY_FILE):
        print("No TSLA position found — deleting stale entry file.")
        os.remove(ENTRY_FILE)


    entry_price = load_entry_price()
    current_price = get_current_price(SYMBOL)

    if entry_price and has_tsla:
        action = should_sell(entry_price, current_price, take_profit * 100, stop_loss * 100)
        if action:
            place_sell_order(SYMBOL)
            log_event(0.0, f"sell_{action}", 0.0)
            os.remove(ENTRY_FILE)
            return

    elif entry_price and not has_tsla:
        print("Entry file exists but no TSLA held. Cleaned up.")

    signal = should_buy()
    if signal:
        amount = calculate_trade_amount(account)
        place_buy_order(SYMBOL, amount)
        log_event(0.0, "buy", amount)
        save_entry_price(current_price)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FAILSAFE] Bot crashed: {str(e)}")
        log_event(0.0, f"ERROR: {str(e)}", 0.0)
        send_email_alert("Alpaca Bot Error", f"The bot encountered an error:\n\n{str(e)}")
