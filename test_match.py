
import requests
import pandas as pd
from pathlib import Path

# Locate project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load completed fixtures
csv_path = BASE_DIR / "data/raw/premier_league_mw1_10_completed.csv"
df = pd.read_csv(csv_path)

# Select the first completed match
match_id = df.iloc[0]["match_id"]

url = "https://www.fotmob.com/api/data/match"

params = {"id": match_id}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

print("Testing match ID:", match_id)

response = requests.get(
    url,
    params=params,
    headers=headers,
    timeout=30
)

print("Status code:", response.status_code)
response.raise_for_status()

data = response.json()

print("\nTOP-LEVEL API KEYS:")
print(list(data.keys()))

print("\nCHECKING RESPONSE STRUCTURE:")

for key, value in data.items():
    if isinstance(value, dict):
        print(f"{key}: dictionary | keys: {list(value.keys())[:20]}")
    elif isinstance(value, list):
        print(f"{key}: list | records: {len(value)}")
    else:
        print(f"{key}: {type(value).__name__}")
