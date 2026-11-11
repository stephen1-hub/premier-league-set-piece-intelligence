
import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "football_analytics.db"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

SET_PIECE_TYPES = [
    "FromCorner",
    "FreeKick",
    "SetPiece",
    "ThrowInSetPiece"
]


def analyse_set_pieces():

    connection = sqlite3.connect(DB_PATH)

    try:
        shots = pd.read_sql_query(
            "SELECT * FROM shot_data",
            connection
        )

        matches = pd.read_sql_query(
            "SELECT match_id, team FROM match_summary",
            connection
        )

    finally:
        connection.close()

    # Filter our working set-piece categories
    set_pieces = shots[
        shots["situation"].isin(SET_PIECE_TYPES)
    ].copy()

    set_pieces["is_goal"] = (
        set_pieces["eventType"] == "Goal"
    )

    # ----------------------------------
    # 1. ATTACKING PERFORMANCE
    # ----------------------------------

    attacking = set_pieces.groupby("team").agg(
        set_piece_shots=("match_id", "size"),
        set_piece_goals=("is_goal", "sum"),
        available_xg=("expectedGoals", "sum"),
        xg_coverage=("expectedGoals", "count")
    ).reset_index()
    
        # Attacking efficiency metrics

    attacking["conversion_rate"] = (
        attacking["set_piece_goals"] /
        attacking["set_piece_shots"] * 100
    )

    attacking["xg_per_shot"] = (
        attacking["available_xg"] /
        attacking["xg_coverage"]
    )

    attacking["goals_minus_xg"] = (
        attacking["set_piece_goals"] -
        attacking["available_xg"]
    )

    attacking["shots_per_goal"] = (
        attacking["set_piece_shots"] /
        attacking["set_piece_goals"].replace(0, pd.NA)
    )

    attacking = attacking.sort_values(
        "set_piece_shots",
        ascending=False
    )

    # ----------------------------------
    # 2. DEFENSIVE PERFORMANCE
    # ----------------------------------

    # Match each shot to the opposing team
    defensive = set_pieces.merge(
        matches.rename(
            columns={"team": "defending_team"}
        ),
        on="match_id",
        how="inner"
    )

    defensive = defensive[
        defensive["team"] != defensive["defending_team"]
    ].copy()

    defensive_summary = defensive.groupby(
        "defending_team"
    ).agg(
        set_piece_shots_conceded=("match_id", "size"),
        set_piece_goals_conceded=("is_goal", "sum"),
        available_xg_conceded=("expectedGoals", "sum"),
        xg_coverage=("expectedGoals", "count")
    ).reset_index()

    defensive_summary = defensive_summary.sort_values(
        "set_piece_shots_conceded",
        ascending=False
    )
    

    # Defensive efficiency metrics

    defensive_summary["shots_conceded_per_match"] = (
        defensive_summary["set_piece_shots_conceded"] / 10
    )

    defensive_summary["goals_conceded_per_match"] = (
        defensive_summary["set_piece_goals_conceded"] / 10
    )

    defensive_summary["xg_conceded_per_shot"] = (
        defensive_summary["available_xg_conceded"] /
        defensive_summary["xg_coverage"]
    )

    defensive_summary["goals_minus_xg_conceded"] = (
        defensive_summary["set_piece_goals_conceded"] -
        defensive_summary["available_xg_conceded"]
    )

    defensive_summary["shot_concession_conversion_rate"] = (
        defensive_summary["set_piece_goals_conceded"] /
        defensive_summary["set_piece_shots_conceded"] * 100
    )

    # ----------------------------------
    # 3. EXPORT RESULTS
    # ----------------------------------

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    attacking.to_csv(
        OUTPUT_DIR / "team_set_piece_attack.csv",
        index=False
    )

    defensive_summary.to_csv(
        OUTPUT_DIR / "team_set_piece_defence.csv",
        index=False
    )

    print("\nATTACKING PERFORMANCE")
    print("-------------------------")
    print(attacking.to_string(index=False))

    print("\nDEFENSIVE PERFORMANCE")
    print("-------------------------")
    print(defensive_summary.to_string(index=False))

    print("\nANALYSIS SUMMARY")
    print("-------------------------")
    print("Set-piece shots:", len(set_pieces))
    print("Set-piece goals:", set_pieces["is_goal"].sum())
    print("Attacking teams:", attacking["team"].nunique())
    print("Defending teams:", defensive_summary["defending_team"].nunique())

    print("\nAnalytical datasets exported successfully.")


if __name__ == "__main__":
    analyse_set_pieces()
