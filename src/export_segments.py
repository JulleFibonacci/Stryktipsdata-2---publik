import pandas as pd

INPUT_FILE = "value_analysis.csv"
OUTPUT_FILE = "segment_report.csv"


def calculate_roi(profit, bets):
    if bets == 0:
        return 0
    return profit / bets * 100


def analyze_segment(
    df,
    outcome,
    odds_col,
    folk_col,
    value_col,
    odds_min,
    odds_max,
    value_min,
    value_max,
    folk_max=None,
):
    data = df[
        df[odds_col].notna()
        & df[folk_col].notna()
        & df[value_col].notna()
        & df["Outcome"].isin(["1", "X", "2"])
    ].copy()

    data = data[
        (data[odds_col] >= odds_min)
        & (data[odds_col] <= odds_max)
        & (data[value_col] >= value_min)
        & (data[value_col] <= value_max)
    ]

    if folk_max is not None:
        data = data[data[folk_col] <= folk_max]

    data["Won"] = data["Outcome"] == outcome
    data["Profit"] = data.apply(
        lambda row: row[odds_col] - 1 if row["Won"] else -1,
        axis=1
    )

    bets = len(data)
    wins = int(data["Won"].sum())
    profit = float(data["Profit"].sum())

    if bets == 0:
        hit_rate = 0
        avg_odds = 0
    else:
        hit_rate = wins / bets * 100
        avg_odds = data[odds_col].mean()

    return {
        "Outcome": outcome,
        "OddsMin": odds_min,
        "OddsMax": odds_max,
        "ValueMin": value_min,
        "ValueMax": value_max,
        "FolkMax": folk_max,
        "Bets": bets,
        "Wins": wins,
        "HitRate": round(hit_rate, 2),
        "AvgOdds": round(avg_odds, 2),
        "Profit": round(profit, 2),
        "ROI": round(calculate_roi(profit, bets), 2),
    }


def main():
    df = pd.read_csv(INPUT_FILE)

    outcomes = [
        ("1", "Odds1", "Folk1", "ValueDiff1"),
        ("X", "OddsX", "FolkX", "ValueDiffX"),
        ("2", "Odds2", "Folk2", "ValueDiff2"),
    ]

    odds_ranges = [
        (1.5, 2.0),
        (2.0, 3.0),
        (3.0, 5.0),
    ]

    value_ranges = [
        (-25, -15),
        (-15, -5),
        (-5, 5),
        (5, 15),
        (15, 25),
    ]

    folk_caps = [
        None,
        25,
        40,
        60,
    ]

    rows = []

    for outcome, odds_col, folk_col, value_col in outcomes:
        for odds_min, odds_max in odds_ranges:
            for value_min, value_max in value_ranges:
                for folk_max in folk_caps:
                    result = analyze_segment(
                        df=df,
                        outcome=outcome,
                        odds_col=odds_col,
                        folk_col=folk_col,
                        value_col=value_col,
                        odds_min=odds_min,
                        odds_max=odds_max,
                        value_min=value_min,
                        value_max=value_max,
                        folk_max=folk_max,
                    )

                    if result["Bets"] >= 50:
                        rows.append(result)

    result_df = pd.DataFrame(rows)

    result_df = result_df.sort_values(
        by=["ROI", "Bets"],
        ascending=[False, False]
    )

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(f"Skapade {OUTPUT_FILE}")
    print(f"Antal segment: {len(result_df)}")
    print()
    print(result_df.head(30).to_string(index=False))


if __name__ == "__main__":
    main()