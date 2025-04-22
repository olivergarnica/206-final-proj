import requests
from datetime import date, timedelta

# Finnhub API setup
FH_KEY = "cvvi5n1r01qi0bq5g0c0cvvi5n1r01qi0bq5g0cg"
START_DATE = "2024-05-10"
END_DATE = "2025-04-15"

# Stock tickers by cap level
stock_tickers = {
    "Highcap": ["AAPL", "MSFT", "GOOGL", "META"],
    "Midcap": ["DOCU", "TWLO", "ZM", "TEAM"],
    "Lowcap": ["PLTR", "ADBE"]
}

def get_all_insider_trades(symbol):
    url = "https://finnhub.io/api/v1/stock/insider-transactions"
    params = {
        "symbol": symbol,
        "token": FH_KEY,
        "from": START_DATE,
        "to": END_DATE
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json().get("data", [])
    return data
