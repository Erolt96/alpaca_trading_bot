import csv
from datetime import datetime
import os

LOG_FILE = "trade_log.csv"


def log_event(price_change, signal, trade_amount):
    """
    Log signal check and trade info to CSV file.
    """
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            # Write header if file is new
            writer.writerow(["timestamp", "price_change_%", "signal", "trade_amount_usd"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            round(price_change, 2) if price_change is not None else "N/A",
            signal,
            round(trade_amount, 2) if trade_amount > 0 else 0
        ])

