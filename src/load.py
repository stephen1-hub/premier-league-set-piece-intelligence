
import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"
DATABASE_DIR = BASE_DIR / "data"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATABASE_DIR / "football_analytics.db"


def load_data():

    summary = pd.read_csv(
        PROCESSED_DIR / "match_summary_clean.csv"
    )

    shots = pd.read_csv(
        PROCESSED_DIR / "shot_data_clean.csv"
    )

    connection = sqlite3.connect(DB_PATH)

    try:
        summary.to_sql(
            "match_summary",
            connection,
            if_exists="replace",
            index=False
        )

        shots.to_sql(
            "shot_data",
            connection,
            if_exists="replace",
            index=False
        )

        print("\nDATABASE LOAD COMPLETE")
        print("-------------------------")
        print("Database:", DB_PATH)

        for table in ["match_summary", "shot_data"]:

            count = pd.read_sql_query(
                f"SELECT COUNT(*) AS total FROM {table}",
                connection
            )["total"].iloc[0]

            print(f"{table}: {count} records")

    finally:
        connection.close()


if __name__ == "__main__":
    load_data()
