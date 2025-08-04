def should_sell(entry_price, current_price, take_profit_pct=3, stop_loss_pct=2):
    change_pct = ((current_price - entry_price) / entry_price) * 100
    if change_pct >= take_profit_pct:
        return "take_profit"
    elif change_pct <= -stop_loss_pct:
        return "stop_loss"
    return None
