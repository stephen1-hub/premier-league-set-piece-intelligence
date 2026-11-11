
import requests
import pandas as pd
import json
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

# FotMob Premier League endpoint
URL = "https://www.fotmob.com/api/data/leagues"

PARAMS = {"id": 47}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


def extract_fixtures():

    print("Connecting to FotMob...")

    response = requests.get(
        URL,
        params=PARAMS,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    # Confirm season
    season = data.get("details", {}).get("selectedSeason")
    print(f"Season: {season}")

    # Get all fixtures
    matches = data["fixtures"]["allMatches"]

    print(f"Total fixtures retrieved: {len(matches)}")

    # Save original fixture response
    raw_file = RAW_DIR / "premier_league_fixtures_raw.json"

    with open(raw_file, "w", encoding="utf-8") as file:
        json.dump(matches, file, indent=4)

    print(f"Raw fixtures saved: {raw_file}")

    # Filter Matchweeks 1–10
    filtered_matches = []

    for match in matches:

        matchweek = int(match.get("round", 0))
        status = match.get("status", {})

        if 1 <= matchweek <= 10 and status.get("finished") is True:

            filtered_matches.append({
                "matchweek": matchweek,
                "match_id": match.get("id"),
                "date": status.get("utcTime"),
                "home_team": match.get("home", {}).get("name"),
                "away_team": match.get("away", {}).get("name"),
                "score": status.get("scoreStr"),
                "finished": status.get("finished"),
                "match_url": match.get("pageUrl")
            })

    # Convert to DataFrame
    df = pd.DataFrame(filtered_matches)

    if not df.empty:
        df = df.sort_values(
            ["matchweek", "date"]
        ).reset_index(drop=True)

    # Export completed matches
    output_file = RAW_DIR / "premier_league_mw1_10_completed.csv"

    df.to_csv(output_file, index=False)

    # Summary
    print("\nEXTRACTION SUMMARY")
    print("-------------------------")
    print(f"Completed matches: {len(df)}")
    print(f"Matchweeks covered: {sorted(df['matchweek'].unique()) if not df.empty else []}")
    print(f"Output: {output_file}")

    if not df.empty:
        print("\nMatches per matchweek:")
        print(df.groupby("matchweek").size())

    return df


if __name__ == "__main__":
    extract_fixtures()