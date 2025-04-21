import requests

MS_KEY = "34963469d75cf929279dacad14cca36d"  

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
