
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(
    DATA_DIR / "team_set_piece_performance.csv"
)

# 1. Attack vs Defence

# 1. Attack vs Defence
plt.figure(figsize=(14, 9))

plt.scatter(
    df["set_piece_goals"],
    df["set_piece_goals_conceded"],
    s=110,
    alpha=0.8
)

# Reference lines: league averages
avg_goals = df["set_piece_goals"].mean()
avg_conceded = df["set_piece_goals_conceded"].mean()

plt.axvline(avg_goals, linestyle="--", alpha=0.6)
plt.axhline(avg_conceded, linestyle="--", alpha=0.6)

# Team labels
for _, row in df.iterrows():
    plt.annotate(
        row["team"],
        (
            row["set_piece_goals"],
            row["set_piece_goals_conceded"]
        ),
        fontsize=8,
        xytext=(7, 6),
        textcoords="offset points"
    )

plt.xlabel("Set-piece Goals Scored")
plt.ylabel("Set-piece Goals Conceded")
plt.title(
    "Premier League Set-Piece Performance | Matchweeks 1–10",
    fontsize=15,
    pad=18
)

plt.text(
    0.02, 0.98,
    "Lower left: Lower scoring and fewer conceded\n"
    "Upper right: Higher scoring and more conceded",
    transform=plt.gca().transAxes,
    va="top",
    fontsize=9
)

plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    REPORT_DIR / "attack_vs_defence.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# 2. Attacking efficiency
attack = df.sort_values(
    "conversion_rate",
    ascending=True
)

plt.figure(figsize=(11, 8))

plt.barh(
    attack["team"],
    attack["conversion_rate"]
)

plt.xlabel("Shot Conversion Rate (%)")
plt.title("Set-piece Attacking Conversion Rate")
plt.tight_layout()
plt.savefig(REPORT_DIR / "attacking_efficiency.png", dpi=300)
plt.close()

# 3. Defensive vulnerability
defence = df.sort_values(
    "set_piece_goals_conceded",
    ascending=True
)

plt.figure(figsize=(11, 8))

plt.barh(
    defence["team"],
    defence["set_piece_goals_conceded"]
)

plt.xlabel("Set-piece Goals Conceded")
plt.title("Set-piece Defensive Vulnerability")
plt.tight_layout()
plt.savefig(REPORT_DIR / "defensive_vulnerability.png", dpi=300)
plt.close()

print("Visualisations generated successfully.")
print("Saved to:", REPORT_DIR)
