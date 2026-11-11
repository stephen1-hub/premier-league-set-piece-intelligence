
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

MATCH_URL = "https://www.fotmob.com/match/5795363"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html"
}


def extract_match(match_id):

    url = f"https://www.fotmob.com/match/{match_id}"

    print(f"Extracting match: {match_id}")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    script = soup.find("script", id="__NEXT_DATA__")

    if script is None:
        raise ValueError("FotMob match data was not found.")

    page_data = json.loads(script.string)

    page_props = page_data["props"]["pageProps"]

    general = page_props["general"]
    content = page_props["content"]

    print("\nMATCH INFORMATION")
    print("-------------------------")
    print("Match:", general["matchName"])
    print("Match ID:", general["matchId"])
    print("League:", general["leagueName"])
    print("Matchweek:", general["matchRound"])

    # Inspect team information
    print("\nHOME TEAM:")
    print(general["homeTeam"])

    print("\nAWAY TEAM:")
    print(general["awayTeam"])

    # Inspect shotmap
    shots = content.get("shotmap", {}).get("shots", [])

    print("\nSHOTMAP")
    print("-------------------------")
    print("Total shots:", len(shots))

    if shots:
        shots_df = pd.DataFrame(shots)

        print("\nShot situations:")
        print(shots_df["situation"].value_counts(dropna=False))

    # Inspect match statistics
    stats = (
        content.get("stats", {})
        .get("Periods", {})
        .get("All", {})
        .get("stats", [])
    )

    print("\nMATCH STATISTICS")
    print("-------------------------")

    for group in stats:

        for item in group.get("stats", []):

            title = item.get("title", "")

            if title in [
                "Corners",
                "xG",
                "xG set play",
                "xG open play"
            ]:
                print(title, item.get("stats"))

    return page_props


if __name__ == "__main__":
    extract_match(5795363)
