import pandas as pd

INPUT_FILE = "english_football_data.csv"


def calculate_roi(df, outcome, odds_col):
    data = df[
        df[odds_col].notna()
        & df["Outcome"].isin(["1", "X", "2"])
    ].copy()

    data["Won"] = data["Outcome"] == outcome

    data["Profit"] = data.apply(
        lambda row: row[odds_col] - 1 if row["Won"] else -1,
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

    summary["HitRate"] = summary["HitRate"] * 100
    summary["ROI"] = summary["Profit"] / summary["Bets"] * 100

    return summary.reset_index().round(2)


def main():
    df = pd.read_csv(INPUT_FILE)

    for col in ["Odds1", "OddsX", "Odds2"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    analyses = [
        ("1", "Odds1", "Hemmalag"),
        ("X", "OddsX", "Kryss"),
        ("2", "Odds2", "Bortalag"),
    ]

    for outcome, odds_col, label in analyses:
        print()
        print("=" * 100)
        print(f"ROI efter oddsintervall: {label}")
        print("=" * 100)

        summary = calculate_roi(
            df=df,
            outcome=outcome,
            odds_col=odds_col
        )

        print(summary.to_string(index=False))

    print()
    print("Klar.")


if __name__ == "__main__":
    main()