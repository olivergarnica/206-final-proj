import requests

ECONDB_BASE_URL = "https://www.econdb.com/api/series/"
ECONDB_TOKEN = "9b26b5d5fc3c3cd3bd0aca58d14a871215020ff3"

ECONDB_SERIES = {
    "RGDPUS": "RGDPUS",  # Real GDP (quarterly)
    "CPIUS": "CPIUS",    # Consumer Price Index (monthly)
    "URATEUS": "URATEUS", # Unemployment rate (monthly)
    "POLIRUS": "POLIRUS", # Fed Short Term Inflation Rate (monthly)
    "Y10YDUS": "Y10YDUS" # 10-year interest Rate (monthly)
}

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

            # Process differently based on the code
            dates = json_data["data"]["dates"]
            values = json_data["data"]["values"]

            if code == "RGDPUS":
                # Get latest 4 quarters
                dates = dates[-4:]
                values = values[-4:]
            elif code in ("CPIUS", "URATEUS", "POLIRUS", "Y10YDUS"):
                # Get latest 12 months
                dates = dates[-12:]
                values = values[-12:]

            # Overwrite the json_data with trimmed data
            json_data["data"]["dates"] = dates
            json_data["data"]["values"] = values

            combined_data["series"].append(json_data)
        else:
            print(f"Failed to fetch {code}: {response.status_code}")
    return combined_data
