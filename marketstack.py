import requests

MS_KEY = "b7a17ae1fb3914c63bb1dde8980687f5"  

def fetch_marketstack_data(symbol, limit=25):
    url = "http://api.marketstack.com/v1/eod"
    params = {
        "access_key": MS_KEY,
        "symbols": symbol,
        "limit": limit
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {symbol}: {response.status_code}")
        return {"data": []}
