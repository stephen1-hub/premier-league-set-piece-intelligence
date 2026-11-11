# Premier League Set-Piece Intelligence

**An end-to-end football data engineering and analytics project exploring set-piece performance across the Premier League 2026/27 season using FotMob data.**

## Project Overview

Set pieces can be an important source of goals and scoring opportunities in football. This project investigates how Premier League teams create and defend set-piece opportunities across Matchweeks 1–10.

I built an ETL pipeline that extracts match and shot data, transforms and validates the records, loads them into SQLite, and produces analytical datasets for an interactive Streamlit dashboard.

## Project Objectives

- Evaluate team attacking performance from set-piece situations.
- Analyse corner-kick and free-kick shot production.
- Identify teams vulnerable to set-piece shots.
- Compare goals, expected goals (xG), and conversion rates.
- Present findings through data visualisations and an interactive dashboard.

## Dataset Overview

| Metric | Value |
|---|---:|
| Competition | Premier League |
| Season | 2026/27 |
| Matchweeks | 1–10 |
| Completed matches | 100 |
| Team-match records | 200 |
| Total shot records | 2,746 |
| Classified set-piece shots | 788 |
| Goals from classified set-piece shots | 56 |

## ETL Pipeline

The project follows five main stages:

1. **Extract:** Retrieve fixtures, match information, statistics and shot data from FotMob.
2. **Transform:** Clean records, standardise team names, classify shot situations and derive analytical variables.
3. **Load:** Store match summaries and shot records in an SQLite database.
4. **Analyse:** Calculate attacking and defensive performance metrics for each team.
5. **Visualise:** Generate analytical charts and an interactive Streamlit dashboard.

## Set-Piece Classification

The working classification includes these FotMob shot-situation categories:

- `FromCorner`
- `FreeKick`
- `SetPiece`
- `ThrowInSetPiece`

Penalties are excluded from this classification.

## Key Findings

Across the 100-match sample:

- **788 set-piece shots** were recorded.
- **56 goals** came from the classified set-piece shots.
- Overall shot conversion was approximately **7.11%**.
- Brighton and Chelsea jointly recorded the most set-piece goals, with seven each.
- Nottingham Forest recorded the highest set-piece shot volume, with 55 attempts.
- Liverpool and Brentford conceded no goals from classified set-piece shots in this sample.
- Crystal Palace conceded the highest number of classified set-piece shots, with 65.

These findings describe the captured sample and should not be interpreted as a complete measure of every set-piece event in football.

## Interactive Dashboard

The Streamlit application contains five sections:

- **Overview:** Key performance indicators and overall team comparisons.
- **Attacking Analysis:** Set-piece shots, goals, conversion and xG.
- **Defensive Analysis:** Set-piece shots and goals conceded.
- **Team Comparison:** Compare selected teams' attacking and defensive output.
- **Methodology:** Data source, classification and analytical limitations.

## Technology Stack

- Python
- Pandas
- NumPy
- Requests
- BeautifulSoup
- SQLite
- Matplotlib
- Plotly
- Streamlit
- Git and GitHub

## Project Structure

```text
fotmob_setpiece_etl/
│
├── app60.py
├── extract_match_data.py
├── test_match.py
├── requirements.txt
├── README.md
│
├── data/
│   └── processed/
│
├── reports/
│   ├── attack_vs_defence.png
│   ├── attacking_efficiency.png
│   └── defensive_vulnerability.png
│
└── src/
    ├── analyse.py
    ├── build_team_report.py
    ├── extract.py
    ├── extract_match_data.py
    ├── load.py
    ├── main.py
    ├── test_match.py
    ├── transform.py
    ├── validate.py
    └── visualise.py
```

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/stephen1-hub/premier-league-set-piece-intelligence.git
cd premier-league-set-piece-intelligence
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

On Windows PowerShell, use:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Dashboard

```bash
streamlit run app60.py
```

The dashboard uses the processed team performance dataset located at:

`data/processed/team_set_piece_performance.csv`

## Methodological Considerations

- The analysis covers only the first ten matchweeks.
- The set-piece classification uses selected FotMob shot-situation labels.
- Penalties are excluded.
- Missing shot-level xG values are preserved rather than replaced with zero.
- xG calculations use available shot-level values.
- Defensive metrics are based on classified shots conceded, not every defensive action or set-piece conceded.
- Conversion rates and goals-minus-xG figures should be interpreted cautiously because of the limited sample.

## Data Source

Match and shot data are sourced from FotMob.

This is an independent football analytics project. FotMob is acknowledged as the source of the underlying match data.

## About the Author

**The Football Data Room**

Football. Data. Intelligence.

Independent football analytics, player scouting, tactical analysis and football data science.

