import pandas as pd

INPUT_FILE = "value_analysis.csv"


def roi(profit, bets):
    if bets == 0:
        return 0

    return (profit / bets) * 100


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
    data = df.copy()

    data = data[
        data[odds_col].notna()
        & data[folk_col].notna()
        & data[value_col].notna()
    ]

    data = data[
        (data[odds_col] >= odds_min)
        & (data[odds_col] <= odds_max)
    ]

    data = data[
        (data[value_col] >= value_min)
        & (data[value_col] <= value_max)
    ]

    if folk_max is not None:
        data = data[
            data[folk_col] <= folk_max
        ]

    data["Won"] = data["Outcome"] == outcome

    data["Profit"] = data.apply(
        lambda row: row[odds_col] - 1
        if row["Won"]
        else -1,
        axis=1
    )

    bets = len(data)

    wins = data["Won"].sum()

    hit_rate = (
        wins / bets * 100
        if bets > 0
        else 0
    )

    total_profit = data["Profit"].sum()

    return {
        "Outcome": outcome,
        "OddsRange": f"{odds_min}-{odds_max}",
        "ValueRange": f"{value_min}-{value_max}",
        "FolkMax": folk_max,
        "Bets": bets,
        "Wins": wins,
        "HitRate": round(hit_rate, 2),
        "Profit": round(total_profit, 2),
        "ROI": round(roi(total_profit, bets), 2),
    }


def main():
    df = pd.read_csv(INPUT_FILE)

    segments = []

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

                    if result["Bets"] < 50:
                        continue

                    segments.append(result)

    result_df = pd.DataFrame(segments)

    result_df = result_df.sort_values(
        by="ROI",
        ascending=False
    )

    print()
    print("=" * 100)
    print("TOPPSEGMENT EFTER ROI")
    print("=" * 100)

    print(
        result_df.head(30).to_string(index=False)
    )

    print()
    print("Klar.")


if __name__ == "__main__":
    main()