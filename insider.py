import requests
import finnhub

from datetime import date, timedelta

FH_KEY = "cvvi5n1r01qi0bq5g0c0cvvi5n1r01qi0bq5g0cg"
finnhub_client = finnhub.Client(FH_KEY)

# Stock tickers by cap level
stock_tickers = {
    "Highcap": ["AAPL", "MSFT", "GOOGL", "META"],
    "Midcap": ["DOCU", "TWLO", "ZM", "TEAM"],
    "Lowcap": ["PLTR", "SMG", "ADBE"]
}

def fetch_finnhub_transactions(symbol, api_key, from_date=None, to_date=None, limit=25):
    url = "https://finnhub.io/api/v1/stock/insider-transactions"
    params = {
        "symbol": symbol,
        "token": api_key,
        "limit": limit
    }

    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {symbol}: {response.status_code}")
        return {"data": [], "symbol": symbol}
