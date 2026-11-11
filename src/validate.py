
import sqlite3
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "football_analytics.db"

connection = sqlite3.connect(DB_PATH)


def run_query(title, query):

    print(f"\n{title}")
    print("-" * 60)

    df = pd.read_sql_query(query, connection)
    print(df.to_string(index=False))

    return df


# 1. Confirm database record counts
run_query(
    "DATABASE RECORD COUNTS",
    """
    SELECT 'match_summary' AS table_name, COUNT(*) AS records
    FROM match_summary

    UNION ALL

    SELECT 'shot_data', COUNT(*)
    FROM shot_data;
    """
)


# 2. Match coverage by matchweek
run_query(
    "MATCHES BY MATCHWEEK",
    """
    SELECT
        matchweek,
        COUNT(DISTINCT match_id) AS matches,
        COUNT(*) AS team_records
    FROM match_summary
    GROUP BY matchweek
    ORDER BY matchweek;
    """
)


# 3. Shot situations and goals
run_query(
    "SHOT SITUATION ANALYSIS",
    """
    SELECT
        situation,
        COUNT(*) AS shots,
        SUM(is_goal) AS goals,
        ROUND(SUM(expectedGoals), 3) AS available_xg
    FROM shot_data
    GROUP BY situation
    ORDER BY shots DESC;
    """
)


# 4. Team-level corner and free-kick output
run_query(
    "TEAM CORNER AND FREE-KICK PERFORMANCE",
    """
    SELECT
        team,
        SUM(corners) AS corners,
        SUM(corner_shots) AS corner_shots,
        SUM(corner_goals) AS corner_goals,
        SUM(free_kick_shots) AS free_kick_shots,
        SUM(free_kick_goals) AS free_kick_goals
    FROM match_summary
    GROUP BY team
    ORDER BY corner_shots DESC;
    """
)


# 5. Check missing xG
run_query(
    "MISSING xG CHECK",
    """
    SELECT
        COUNT(*) AS total_shots,
        SUM(CASE
            WHEN expectedGoals IS NULL THEN 1
            ELSE 0
        END) AS missing_xg,
        SUM(is_goal) AS total_goals
    FROM shot_data;
    """
)


connection.close()

print("\nSQL VALIDATION COMPLETED.")
