import requests

ECONDB_BASE_URL = "https://www.econdb.com/api/series/"
ECONDB_TOKEN = "9b26b5d5fc3c3cd3bd0aca58d14a871215020ff3"

ECONDB_SERIES = {
    "RGDPUS": "RGDPUS",
    "CPIUS": "CPIUS",
}

def fetch_econdb_data(series_codes=None):
    if series_codes is None:
        series_codes = ECONDB_SERIES.values()

    combined_data = {"series": []}
    for code in series_codes:
        url = f"{ECONDB_BASE_URL}{code}/?format=json&token={ECONDB_TOKEN}"
        print(url)
        response = requests.get(f"{ECONDB_BASE_URL}{code}/?format=json&token={ECONDB_TOKEN}")
        if response.status_code == 200:
            json_data = response.json()
            combined_data["series"].append(json_data)
        else:
            print(f"Failed to fetch {code}: {response.status_code}")
    return combined_data
