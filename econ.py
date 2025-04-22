import requests

ECONDB_BASE_URL = "https://www.econdb.com/api/series/"
ECONDB_TOKEN = "9b26b5d5fc3c3cd3bd0aca58d14a871215020ff3"

ECONDB_SERIES = {
    "RGDPUS": "RGDPUS",   # Real GDP (quarterly)
    "CPIUS": "CPIUS",     # Consumer Price Index (monthly)
    "URATEUS": "URATEUS", # Unemployment rate (monthly)
    "POLIRUS": "POLIRUS", # Short term policy rate (monthly)
    "Y10YDUS": "Y10YDUS", # 10-year interest Rate (monthly)
    "PPIUS": "PPIUS",     # Producer Price Index (monthly)
    "RPUCUS": "RPUCUS",   # Real public consumption (quarterly)
    "M3YDUS": "M3YDUS",   # 3 month yield (monthly)
    "GDEBTUS": "GDEBTUS", # Government debt (monthly)
    "RIMPUS": "RIMPUS",   # Real imports (quarterly)
    "REXPUS": "REXPUS"    # Real exports (quarterly)
}

# Group quarterly and monthly series
QUARTERLY_SERIES = {"RGDPUS", "RPUCUS", "RIMPUS", "REXPUS"}
MONTHLY_SERIES = {"CPIUS", "URATEUS", "POLIRUS", "Y10YDUS", "PPIUS", "M3YDUS", "GDEBTUS"}

def fetch_econdb_data(series_codes=None):
    if series_codes is None:
        series_codes = ECONDB_SERIES.values()

    combined_data = {"series": []}
    for code in series_codes:
        url = f"{ECONDB_BASE_URL}{code}/?format=json&token={ECONDB_TOKEN}"
        print(f"Fetching {code} from {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()

            dates = json_data["data"]["dates"]
            values = json_data["data"]["values"]

            # Trim based on frequency
            if code in QUARTERLY_SERIES:
                dates = dates[-4:]  # Latest 4 quarters
                values = values[-4:]
            elif code in MONTHLY_SERIES:
                dates = dates[-12:]  # Latest 12 months
                values = values[-12:]

            # Save the trimmed data
            json_data["data"]["dates"] = dates
            json_data["data"]["values"] = values

            combined_data["series"].append(json_data)
        else:
            print(f"Failed to fetch {code}: {response.status_code}")
    return combined_data
