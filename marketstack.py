import requests

MS_KEY = "f37d82be3c3a6f869b22b6a6a3a5752c"  
def fetch_marketstack_data(symbol, limit=1000, date_from="2024-05-13", date_to="2025-04-21"):
    url = "http://api.marketstack.com/v1/eod"
    params = {
        "access_key": MS_KEY,
        "symbols": symbol,
        "limit": limit,
        "date_from": date_from,
        "date_to": date_to
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {symbol}: {response.status_code}")
        return {"data": []}
