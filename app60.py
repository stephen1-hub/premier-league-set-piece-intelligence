
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Premier League Set-Piece Intelligence",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #101820;
        color: #FFFFFF;
    }

    [data-testid="stSidebar"] {
        background-color: #182A38;
    }

    h1, h2, h3 {
        color: #FFFFFF;
    }

    [data-testid="stMetricValue"] {
        color: #16A34A;
    }

    [data-testid="stMetricLabel"] {
        color: #A7B4C2;
    }

    .stCaption {
        color: #A7B4C2;
    }

    hr {
        border-color: #34495A;
    }

    [data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] {
    background-color: #182A38;
}

.stRadio label {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        DATA_DIR / "team_set_piece_performance.csv"
    )
    return df

df = load_data()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("⚽ Premier League Set-Piece Intelligence")

st.markdown(
    "### Matchweeks 1–10 | 2026/27 Season"
)

st.caption(
    "An independent football analytics investigation "
    "using match and shot data collected from FotMob."
)

st.divider()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Dashboard Navigation")

section = st.sidebar.radio(
    "Select Analysis",
    [
        "Overview",
        "Attacking Analysis",
        "Defensive Analysis",
        "Team Comparison",
        "Methodology"
    ]
)

# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if section == "Overview":

    st.subheader("League Set-Piece Overview")

    total_shots = df["set_piece_shots"].sum()
    total_goals = df["set_piece_goals"].sum()
    total_conceded = df["set_piece_goals_conceded"].sum()

    conversion = (
        total_goals / total_shots * 100
        if total_shots else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Set-Piece Shots", f"{total_shots:,}")
    col2.metric("Set-Piece Goals", f"{total_goals:,}")
    col3.metric("Overall Conversion", f"{conversion:.2f}%")
    col4.metric("Teams Analysed", len(df))

    st.divider()

    left, right = st.columns(2)

    with left:
        st.markdown("#### Top Set-Piece Scoring Teams")

        top_attack = df.sort_values(
            "set_piece_goals",
            ascending=False
        ).head(10)

        fig = px.bar(
            top_attack,
            x="set_piece_goals",
            y="team",
            orientation="h",
            title="Set-Piece Goals Scored",
            labels={
                "set_piece_goals": "Goals",
                "team": "Team"
            }
        )
        
        fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#182A38",
        plot_bgcolor="#182A38",
        font=dict(color="#FFFFFF"),
        title_font=dict(color="#FFFFFF"),
        xaxis=dict(
        title_font=dict(color="#A7B4C2"),
        tickfont=dict(color="#A7B4C2"),
        gridcolor="#34495A"
        ),
        yaxis=dict(
        title_font=dict(color="#A7B4C2"),
        tickfont=dict(color="#A7B4C2"),
        gridcolor="#34495A"
       )
       )

        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("#### Most Set-Piece Goals Conceded")

        top_defence = df.sort_values(
            "set_piece_goals_conceded",
            ascending=False
        ).head(10)

        fig = px.bar(
            top_defence,
            x="set_piece_goals_conceded",
            y="team",
            orientation="h",
            title="Set-Piece Goals Conceded",
            labels={
                "set_piece_goals_conceded": "Goals Conceded",
                "team": "Team"
            }
        )
        fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#182A38",
    plot_bgcolor="#182A38",
    font=dict(color="#FFFFFF"),
    title_font=dict(color="#FFFFFF"),
    xaxis=dict(
        title_font=dict(color="#A7B4C2"),
        tickfont=dict(color="#A7B4C2"),
        gridcolor="#34495A"
    ),
    yaxis=dict(
        title_font=dict(color="#A7B4C2"),
        tickfont=dict(color="#A7B4C2"),
        gridcolor="#34495A"
    )
    )
        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

    st.subheader("What the Data Tells Us")

    insight1, insight2, insight3 = st.columns(3)

    with insight1:
        st.markdown("**Most clinical attack**")
        st.metric("Chelsea", "17.50%", "Conversion rate")

    with insight2:
        st.markdown("**Highest scoring output**")
        st.metric("Brighton & Chelsea", "7 goals", "Joint leaders")

    with insight3:
        st.markdown("**Best defensive record**")
        st.metric("Liverpool & Brentford", "0 goals", "Conceded")

    st.caption(
        "Findings cover the first ten matchweeks only. "
        "These are descriptive results, not long-term performance claims."
    )
    st.markdown("#### Team Performance Dataset")

    st.markdown("#### Team Performance Dataset")

    st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    height=450,
    column_config={
        "team": st.column_config.TextColumn("Team"),
        "set_piece_shots": st.column_config.NumberColumn("Shots"),
        "set_piece_goals": st.column_config.NumberColumn("Goals"),
        "conversion_rate": st.column_config.NumberColumn(
            "Conversion (%)",
            format="%.2f"
        ),
        "set_piece_shots_conceded": st.column_config.NumberColumn(
            "Shots Conceded"
        ),
        "set_piece_goals_conceded": st.column_config.NumberColumn(
            "Goals Conceded"
        )
    }
)

# --------------------------------------------------
# ATTACKING ANALYSIS
# --------------------------------------------------

elif section == "Attacking Analysis":

    st.subheader("Set-Piece Attacking Performance")

    metric = st.selectbox(
        "Choose attacking metric",
        [
            "set_piece_goals",
            "set_piece_shots",
            "conversion_rate",
            "available_xg",
            "xg_per_shot"
        ],
        format_func=lambda x: {
            "set_piece_goals": "Goals Scored",
            "set_piece_shots": "Shots",
            "conversion_rate": "Conversion Rate (%)",
            "available_xg": "Available xG",
            "xg_per_shot": "xG per Shot"
        }[x]
    )

    attacking = df.sort_values(
        metric,
        ascending=False
    )

    
    fig = px.bar(
    attacking.sort_values(metric, ascending=True),
    x=metric,
    y="team",
    orientation="h",
    title="Team Attacking Performance",
    text=metric,
    labels={
        metric: metric.replace("_", " ").title(),
        "team": "Team"
    },
    color_discrete_sequence=["#16A34A"]
    )

   
    fig.update_traces(
    textposition="outside",
    texttemplate=(
        "%{x:.0f}"
        if metric in ["set_piece_shots", "set_piece_goals"]
        else "%{x:.2f}"
    ),
    cliponaxis=False
    )


    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#182A38",
    plot_bgcolor="#182A38",
    font=dict(color="#FFFFFF"),
    title_font=dict(color="#FFFFFF", size=18),
    showlegend=False,
    xaxis=dict(
        title=metric.replace("_", " ").title(),
        gridcolor="#34495A"
    ),
    yaxis=dict(
        title="",
        gridcolor="#34495A"
    ),
    margin=dict(l=20, r=60, t=60, b=40)
    )

    
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Attacking Efficiency")

    st.dataframe(
        df[[
            "team",
            "set_piece_shots",
            "set_piece_goals",
            "available_xg",
            "conversion_rate",
            "xg_per_shot",
            "goals_minus_xg"
        ]].sort_values(
            "set_piece_goals",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# DEFENSIVE ANALYSIS
# --------------------------------------------------

elif section == "Defensive Analysis":

    st.subheader("Set-Piece Defensive Performance")

    metric = st.selectbox(
        "Choose defensive metric",
        [
            "set_piece_shots_conceded",
            "set_piece_goals_conceded",
            "available_xg_conceded",
            "shots_conceded_per_match",
            "goals_conceded_per_match"
        ],
        format_func=lambda x: {
            "set_piece_shots_conceded": "Shots Conceded",
            "set_piece_goals_conceded": "Goals Conceded",
            "available_xg_conceded": "Available xG Conceded",
            "shots_conceded_per_match": "Shots Conceded per Match",
            "goals_conceded_per_match": "Goals Conceded per Match"
        }[x]
    )

    defensive = df.sort_values(
        metric,
        ascending=False
    )

    
    fig = px.bar(
    defensive.sort_values(metric, ascending=True),
    x=metric,
    y="team",
    orientation="h",
    title="Set-Piece Defensive Vulnerability",
    text=metric,
    labels={
        metric: metric.replace("_", " ").title(),
        "team": "Team"
    },
    color_discrete_sequence=["#16A34A"]
    )

    fig.update_traces(
    textposition="outside",
    texttemplate=(
        "%{x:.0f}"
        if metric in [
            "set_piece_shots_conceded",
            "set_piece_goals_conceded"
        ]
        else "%{x:.2f}"
    ),
    cliponaxis=False
    )

    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#182A38",
    plot_bgcolor="#182A38",
    font=dict(color="#FFFFFF"),
    title_font=dict(color="#FFFFFF", size=18),
    showlegend=False,
    xaxis=dict(
        title=metric.replace("_", " ").title(),
        gridcolor="#34495A"
    ),
    yaxis=dict(
        title="",
        gridcolor="#34495A"
    ),
    margin=dict(l=20, r=60, t=60, b=40)
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        df[[
            "team",
            "set_piece_shots_conceded",
            "set_piece_goals_conceded",
            "available_xg_conceded",
            "xg_conceded_per_shot",
            "goals_minus_xg_conceded"
        ]].sort_values(
            "set_piece_goals_conceded",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# TEAM COMPARISON
# --------------------------------------------------


elif section == "Team Comparison":

    st.subheader("Compare Team Performance")

    teams = sorted(df["team"].unique())

    selected_teams = st.multiselect(
        "Select teams to compare",
        teams,
        default=[
            "Chelsea",
            "Brighton & Hove Albion",
            "Manchester City"
        ]
    )

    if selected_teams:

        comparison = df[
            df["team"].isin(selected_teams)
        ].copy()

        fig = px.scatter(
            comparison,
            x="set_piece_goals",
            y="set_piece_goals_conceded",
            size="set_piece_shots",
            color="team",
            hover_name="team",
            text="team",
            title="Set-Piece Attack vs Defence",
            labels={
                "set_piece_goals": "Set-Piece Goals Scored",
                "set_piece_goals_conceded": "Set-Piece Goals Conceded",
                "set_piece_shots": "Set-Piece Shots"
            },
            size_max=35
        )

        fig.update_traces(
            textposition="top center",
            textfont=dict(color="#FFFFFF", size=11),
            marker=dict(
                line=dict(color="#FFFFFF", width=1)
            )
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#182A38",
            plot_bgcolor="#182A38",
            font=dict(color="#FFFFFF"),
            title_font=dict(color="#FFFFFF", size=18),
            xaxis=dict(
                title="Set-Piece Goals Scored",
                gridcolor="#34495A"
            ),
            yaxis=dict(
                title="Set-Piece Goals Conceded",
                gridcolor="#34495A"
            ),
            legend_title_text="Teams",
            margin=dict(l=30, r=30, t=65, b=45)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("#### Team Comparison Data")

        st.dataframe(
            comparison[[
                "team",
                "set_piece_shots",
                "set_piece_goals",
                "conversion_rate",
                "set_piece_shots_conceded",
                "set_piece_goals_conceded"
            ]],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Select at least one team to compare.")

# --------------------------------------------------
# METHODOLOGY
# --------------------------------------------------

elif section == "Methodology":

    st.subheader("Data & Analytical Methodology")

    st.markdown("""
    **Data source:** FotMob

    **Competition:** Premier League 2026/27

    **Coverage:** Matchweeks 1–10, 100 completed matches.

    **Data processing pipeline:**
    1. Extract match fixtures and shot-level data.
    2. Clean and standardise team and event information.
    3. Load processed records into SQLite.
    4. Classify set-piece shots.
    5. Calculate team attacking and defensive metrics.
    6. Generate analytical datasets and visualisations.

    **Working set-piece shot classification:**
    - FromCorner
    - FreeKick
    - SetPiece
    - ThrowInSetPiece

    Penalties are excluded from this working classification.

    **Important limitations:**
    - The analysis is based on captured shot events.
    - Available xG excludes shots with missing xG values.
    - Ten matchweeks represent a limited sample.
    - Defensive shot counts do not represent every defensive action.
    - Set-piece classification is based on the shot-situation categories available in FotMob. It represents the working classification used in this analysis and may not capture every possible set-piece event.
    """)

    st.info(
        "The findings describe performance in the observed "
        "sample and should not be interpreted as proof of "
        "long-term team tendencies."
    )

st.divider()

st.caption(
    "THE FOOTBALL DATA ROOM | Football. Data. Intelligence."
)
