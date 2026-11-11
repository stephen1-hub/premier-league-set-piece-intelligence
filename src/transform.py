
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def transform_data():

    summary = pd.read_csv(
        PROCESSED_DIR / "match_summary_mw1_10.csv"
    )

    shots = pd.read_csv(
        PROCESSED_DIR / "shot_data_mw1_10.csv"
    )

    # Standardise text columns
    summary["team"] = summary["team"].str.strip()
    shots["team"] = shots["team"].str.strip()

    shots["situation"] = shots["situation"].str.strip()
    shots["eventType"] = shots["eventType"].str.strip()

    # Preserve missing xG values
    shots["expectedGoals"] = pd.to_numeric(
        shots["expectedGoals"],
        errors="coerce"
    )

    # Create explicit shot classification flags
    shots["is_goal"] = shots["eventType"].eq("Goal")

    shots["is_corner_shot"] = (
        shots["situation"].eq("FromCorner")
    )

    shots["is_free_kick_shot"] = (
        shots["situation"].eq("FreeKick")
    )

    shots["is_set_piece_shot"] = (
        shots["situation"].isin([
            "FromCorner",
            "SetPiece",
            "ThrowInSetPiece",
            "FreeKick"
        ])
    )

    # Export cleaned datasets
    summary.to_csv(
        PROCESSED_DIR / "match_summary_clean.csv",
        index=False
    )

    shots.to_csv(
        PROCESSED_DIR / "shot_data_clean.csv",
        index=False
    )

    # Data quality report
    print("\nTRANSFORMATION SUMMARY")
    print("-------------------------")
    print("Match summary rows:", len(summary))
    print("Shot records:", len(shots))
    print("Missing xG:", shots["expectedGoals"].isna().sum())
    print("Goals:", shots["is_goal"].sum())

    print(
        "xG coverage:",
        round(shots["expectedGoals"].notna().mean() * 100, 2),
        "%"
    )

    print("\nSET-PIECE SHOTS")
    print("-------------------------")

    print(
        shots.groupby("situation").agg(
            shots=("eventType", "size"),
            goals=("is_goal", "sum"),
            available_xg=("expectedGoals", "count")
        )
    )

    print("\nClean datasets exported successfully.")


if __name__ == "__main__":
    transform_data()
