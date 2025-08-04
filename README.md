# 🤑 Alpaca Trading Bot 🤑

A Python trading bot for TSLA using the Alpaca API. It runs automatically (every 30minutes for example) and checks the price of TESLA whether to BUY or NOT, if 
we have bought, then it checks to close on TP or SL (based on the % I have selected on python script)

###  Features
- Momentum-based buy signals
- Configurable TP, SL, and risk settings
- Base capital protection
- Reinvests profits
- Logs trades to CSV

### 🔧 Setup
1. Add your API keys in `.env`
2. Adjust settings in `config.json`
3. Install requirements:
```bash
pip install -r requirements.txt
