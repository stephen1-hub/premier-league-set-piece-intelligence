
import requests
import pandas as pd
import json
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data/raw/premier_league_mw1_10_completed.csv"

df = pd.read_csv(csv_path)
match_id = str(df.iloc[0]["match_id"])

url = f"https://www.fotmob.com/match/{match_id}"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
script = soup.find("script", id="__NEXT_DATA__")

page_data = json.loads(script.string)
content = page_data["props"]["pageProps"]["content"]

# 1. Inspect match events
events = content["matchFacts"].get("events")

print("\nMATCH EVENTS")
print("Type:", type(events).__name__)

if isinstance(events, list):
    print("Records:", len(events))
    for event in events[:5]:
        print(json.dumps(event, indent=2)[:1500])

elif isinstance(events, dict):
    print("Keys:", list(events.keys()))
    print(json.dumps(events, indent=2)[:4000])

# 2. Inspect global shotmap
shotmap = content.get("shotmap")

print("\nSHOTMAP")
print("Type:", type(shotmap).__name__)

if isinstance(shotmap, list):
    print("Shots:", len(shotmap))

    for shot in shotmap[:10]:
        print({
            "player": shot.get("playerName"),
            "event": shot.get("eventType"),
            "situation": shot.get("situation"),
            "minute": shot.get("min"),
            "xG": shot.get("expectedGoals")
        })

elif isinstance(shotmap, dict):
    print("Keys:", list(shotmap.keys()))
    print(json.dumps(shotmap, indent=2)[:4000])

# 3. Inspect available match statistics
print("\nMATCH STATISTICS")

for group in content["stats"]["Periods"]["All"]["stats"]:
    print("\n", group["title"])

    for stat in group.get("stats", []):
        print(stat.get("title"), ":", stat.get("stats"))
