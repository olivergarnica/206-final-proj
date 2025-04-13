import requests
import sqlite3
import finnhub

FH_KEY = ""  # INSERT FINNHUB API KEY HERE
finnhub_client = finnhub.Client(FH_KEY)

stock_tickers = {
    "Highcap" : ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "META", "TSM"],
    "Midcap": ["DOCU", "TWLO", "ZM", "NET", "TEAM", "SQ"],
    "Lowcap": ["PLTR", "ZEN", "SMG", "ADBE"]
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
        print("Error", response.status_code)
        return {"data": [], "symbol": symbol}
