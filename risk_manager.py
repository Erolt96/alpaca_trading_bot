from alpaca_api import get_account

import json

with open("config.json", "r") as f:
    config = json.load(f)

BASE_PROTECTION = 50.0  # Still fixed for now
ALLOCATION_PCT = config["allocation_percent"]


def calculate_trade_amount(account):
    """
    Calculates how much USD to use for the trade:
    - Uses 15% of available buying power
    - Ensures BASE_PROTECTION is respected
    """
    if account is None:
        account = get_account()

    equity = float(account.equity)
    buying_power = float(account.buying_power)

    # Make sure we keep base capital safe
    if equity <= BASE_PROTECTION:
        return 0.0

    # Use 15% of available buying power
    trade_amount = (ALLOCATION_PCT / 100) * buying_power

    # Make sure trade amount doesn't bring equity below base
    max_safe_trade = equity - BASE_PROTECTION
    final_amount = min(trade_amount, max_safe_trade)

    return round(max(final_amount, 0.0), 2)
