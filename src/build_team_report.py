
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load analytical datasets
attack = pd.read_csv(
    DATA_DIR / "team_set_piece_attack.csv"
)

defence = pd.read_csv(
    DATA_DIR / "team_set_piece_defence.csv"
)

# Merge attacking and defensive performance
report = attack.merge(
    defence,
    left_on="team",
    right_on="defending_team",
    how="inner"
)

report = report.drop(columns=["defending_team"])

# Add rankings
report["attack_goals_rank"] = (
    report["set_piece_goals"]
    .rank(method="min", ascending=False)
    .astype(int)
)

report["attack_conversion_rank"] = (
    report["conversion_rate"]
    .rank(method="min", ascending=False)
    .astype(int)
)

report["defensive_goals_conceded_rank"] = (
    report["set_piece_goals_conceded"]
    .rank(method="min", ascending=True)
    .astype(int)
)

report["defensive_shots_conceded_rank"] = (
    report["set_piece_shots_conceded"]
    .rank(method="min", ascending=True)
    .astype(int)
)

# Round numeric values
numeric_columns = report.select_dtypes(
    include="number"
).columns

report[numeric_columns] = report[numeric_columns].round(3)

# Export
output_file = DATA_DIR / "team_set_piece_performance.csv"
report.to_csv(output_file, index=False)

print("Combined team report created successfully.")
print("Teams:", len(report))
print("Columns:", len(report.columns))
print(report[[
    "team",
    "set_piece_shots",
    "set_piece_goals",
    "conversion_rate",
    "set_piece_shots_conceded",
    "set_piece_goals_conceded"
]].to_string(index=False))
