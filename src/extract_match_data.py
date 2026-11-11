
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html"
}


def get_match_page(match_id):

    url = f"https://www.fotmob.com/match/{match_id}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("script", id="__NEXT_DATA__")

    if script is None:
        raise ValueError(f"Match data not found for {match_id}")

    page_data = json.loads(script.string)

    return page_data["props"]["pageProps"]


def get_match_statistics(content):

    stats = (
        content.get("stats", {})
        .get("Periods", {})
        .get("All", {})
        .get("stats", [])
    )

    results = {}

    for group in stats:
        for item in group.get("stats", []):

            title = item.get("title")

            if title:
                results[title.lower()] = item.get("stats")

    return results


def extract_match(match_id, matchweek=None):

    print(f"Extracting match: {match_id}")

    page_props = get_match_page(match_id)

    general = page_props["general"]
    content = page_props["content"]

    home = general["homeTeam"]
    away = general["awayTeam"]

    home_id = home["id"]
    away_id = away["id"]

    statistics = get_match_statistics(content)

    shots = content.get("shotmap", {}).get("shots", [])

    shots_df = pd.DataFrame(shots)

    if shots_df.empty:
        shots_df = pd.DataFrame(columns=[
            "teamId", "playerName", "min", "minAdded",
            "situation", "eventType", "expectedGoals"
        ])

    def get_stat(name, index):

        values = statistics.get(name.lower())

        if values and len(values) > index:
            try:
                return float(values[index])
            except (ValueError, TypeError):
                return None

        return None

    def count_shots(team_id, situation, goals_only=False):

        selected = shots_df[
            (shots_df["teamId"] == team_id) &
            (shots_df["situation"] == situation)
        ]

        if goals_only:
            selected = selected[
                selected["eventType"] == "Goal"
            ]

        return len(selected)

    match_summary = []

    for index, team in enumerate([home, away]):

        team_id = team["id"]

        match_summary.append({

            "match_id": match_id,
            "matchweek": matchweek,
            "match_date": general.get("matchTimeUTC"),
            "home_team": home["name"],
            "away_team": away["name"],
            "team": team["name"],
            "venue": "Home" if index == 0 else "Away",

            "corners": get_stat("corners", index),
            "open_play_xg": get_stat("xg open play", index),
            "set_play_xg": get_stat("xg set play", index),

            "corner_shots": count_shots(
                team_id, "FromCorner"
            ),

            "corner_goals": count_shots(
                team_id, "FromCorner", goals_only=True
            ),

            "free_kick_shots": count_shots(
                team_id, "FreeKick"
            ),

            "free_kick_goals": count_shots(
                team_id, "FreeKick", goals_only=True
            )
        })

    # Prepare shot-level dataset
    if not shots_df.empty:

        shots_df = shots_df.copy()

        shots_df["match_id"] = match_id
        shots_df["matchweek"] = matchweek
        shots_df["match_date"] = general.get("matchTimeUTC")

        team_names = {
            home_id: home["name"],
            away_id: away["name"]
        }

        shots_df["team"] = shots_df["teamId"].map(team_names)

        selected_columns = [
            "match_id",
            "matchweek",
            "match_date",
            "team",
            "playerName",
            "min",
            "minAdded",
            "situation",
            "eventType",
            "expectedGoals",
            "isOnTarget",
            "isBlocked"
        ]

        available_columns = [
            col for col in selected_columns
            if col in shots_df.columns
        ]

        shots_df = shots_df[available_columns]

    summary_df = pd.DataFrame(match_summary)

    return summary_df, shots_df



import time
from tqdm import tqdm

if __name__ == "__main__":

    FIXTURES_FILE = RAW_DIR / "premier_league_mw1_10_completed.csv"

    PROCESSED_DIR = BASE_DIR / "data" / "processed"
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    SUMMARY_FILE = PROCESSED_DIR / "match_summary_mw1_10.csv"
    SHOTS_FILE = PROCESSED_DIR / "shot_data_mw1_10.csv"
    ERRORS_FILE = PROCESSED_DIR / "extraction_errors.csv"

    fixtures = pd.read_csv(FIXTURES_FILE)

    print(f"Fixtures loaded: {len(fixtures)}")

    all_summaries = []
    all_shots = []
    errors = []

    for _, fixture in tqdm(
        fixtures.iterrows(),
        total=len(fixtures),
        desc="Extracting matches"
    ):

        match_id = int(fixture["match_id"])
        matchweek = int(fixture["matchweek"])

        try:
            summary, shots = extract_match(
                match_id=match_id,
                matchweek=matchweek
            )

            all_summaries.append(summary)
            all_shots.append(shots)

        except Exception as error:

            print(f"\nFailed match {match_id}: {error}")

            errors.append({
                "match_id": match_id,
                "matchweek": matchweek,
                "error": str(error)
            })

        # Save progress after each match
        if all_summaries:
            pd.concat(
                all_summaries,
                ignore_index=True
            ).to_csv(SUMMARY_FILE, index=False)

        if all_shots:
            pd.concat(
                all_shots,
                ignore_index=True
            ).to_csv(SHOTS_FILE, index=False)

        if errors:
            pd.DataFrame(errors).to_csv(
                ERRORS_FILE,
                index=False
            )

        # Allow a short interval between requests
        time.sleep(1.2)

    print("\nEXTRACTION COMPLETE")
    print("-------------------------")
    print(f"Fixtures processed: {len(fixtures)}")
    print(f"Successful matches: {len(all_summaries)}")
    print(f"Failed matches: {len(errors)}")

    if all_summaries:
        final_summary = pd.read_csv(SUMMARY_FILE)

        print(f"Team summary rows: {len(final_summary)}")
        print(f"Shot records: {len(pd.read_csv(SHOTS_FILE))}")

        print("\nMatches by matchweek:")
        print(
            final_summary.groupby("matchweek")["match_id"]
            .nunique()
        )
