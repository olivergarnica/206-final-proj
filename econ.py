import requests

ECONDB_BASE_URL = "https://www.econdb.com/api/series/"

ECONDB_SERIES = {
    "GDP_USA": "GDP_USA_Q",      # Quarterly GDP
    "CPI_USA": "CP_USA_M",       # Monthly Inflation 
    "IR_USA": "IR_USA_M"         # Monthly Interest Rate
}

def fetch_econdb_data(series_codes=None):
    if series_codes is None:
        series_codes = ECONDB_SERIES.values()

    combined_data = {"datasets": {}}

    for code in series_codes:
        response = requests.get(f"{ECONDB_BASE_URL}{code}/")
        if response.status_code == 200:
            json_data = response.json()
            combined_data["datasets"][code] = json_data.get("data", {})
        else:
            print(f"Failed to fetch {code}: {response.status_code}")

    return combined_data
