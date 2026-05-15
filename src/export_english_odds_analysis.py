import pandas as pd

INPUT_FILE = "english_football_data.csv"
OUTPUT_FILE = "english_odds_analysis.csv"


def calculate_roi(df, outcome, odds_col):
    data = df[
        df[odds_col].notna()
        & df["Outcome"].isin(["1", "X", "2"])
    ].copy()

    data["Won"] = data["Outcome"] == outcome

    data["Profit"] = data.apply(
        lambda row: row[odds_col] - 1
        if row["Won"]
        else -1,
        axis=1
    )

    bins = [1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 15.0, 100.0]
    labels = [
        "1.00-1.50",
        "1.50-2.00",
        "2.00-3.00",
        "3.00-5.00",
        "5.00-8.00",
        "8.00-15.00",
        "15.00+",
    ]

    data["OddsBucket"] = pd.cut(
        data[odds_col],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    summary = data.groupby(
        ["Division", "OddsBucket"],
        observed=False
    ).agg(
        Bets=("Won", "count"),
        Wins=("Won", "sum"),
        HitRate=("Won", "mean"),
        AvgOdds=(odds_col, "mean"),
        Profit=("Profit", "sum"),
    )

    summary["Outcome"] = outcome
    summary["OddsColumn"] = odds_col
    summary["HitRate"] = summary["HitRate"] * 100
    summary["ROI"] = summary["Profit"] / summary["Bets"] * 100

    return summary.reset_index()


def main():
    df = pd.read_csv(INPUT_FILE)

    for col in ["Odds1", "OddsX", "Odds2"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    analyses = [
        ("1", "Odds1"),
        ("X", "OddsX"),
        ("2", "Odds2"),
    ]

    rows = []

    for outcome, odds_col in analyses:
        summary = calculate_roi(
            df=df,
            outcome=outcome,
            odds_col=odds_col
        )

        rows.append(summary)

    result_df = pd.concat(rows, ignore_index=True)

    result_df = result_df[
        [
            "Outcome",
            "OddsColumn",
            "Division",
            "OddsBucket",
            "Bets",
            "Wins",
            "HitRate",
            "AvgOdds",
            "Profit",
            "ROI",
        ]
    ]

    result_df = result_df.round(2)

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(f"Skapade {OUTPUT_FILE}")
    print(f"Antal rader: {len(result_df)}")
    print()
    print(result_df.to_string(index=False))


if __name__ == "__main__":
    main()