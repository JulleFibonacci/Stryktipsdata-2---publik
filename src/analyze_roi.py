import pandas as pd

INPUT_FILE = "value_analysis.csv"


def calculate_roi(df, outcome, odds_col, value_col):
    data = df[
        df[odds_col].notna()
        & df[value_col].notna()
        & df["Outcome"].isin(["1", "X", "2"])
    ].copy()

    data["BetWon"] = data["Outcome"] == outcome

    data["Profit"] = data.apply(
        lambda row: row[odds_col] - 1
        if row["BetWon"]
        else -1,
        axis=1
    )

    bins = [-100, -40, -25, -15, -5, 5, 15, 25, 40, 100]

    labels = [
        "< -40",
        "-40 till -25",
        "-25 till -15",
        "-15 till -5",
        "-5 till +5",
        "+5 till +15",
        "+15 till +25",
        "+25 till +40",
        "> +40",
    ]

    data["ValueBucket"] = pd.cut(
        data[value_col],
        bins=bins,
        labels=labels
    )

    summary = data.groupby(
        "ValueBucket",
        observed=False
    ).agg(
        AntalSpel=("BetWon", "count"),
        Vinster=("BetWon", "sum"),
        Träffprocent=("BetWon", "mean"),
        SnittOdds=(odds_col, "mean"),
        Profit=("Profit", "sum"),
    )

    summary["Träffprocent"] = (
        summary["Träffprocent"] * 100
    )

    summary["ROI"] = (
        summary["Profit"]
        / summary["AntalSpel"]
        * 100
    )

    return summary.round(2)


def main():
    df = pd.read_csv(INPUT_FILE)

    analyses = [
        ("1", "Odds1", "ValueDiff1"),
        ("X", "OddsX", "ValueDiffX"),
        ("2", "Odds2", "ValueDiff2"),
    ]

    for outcome, odds_col, value_col in analyses:

        print()
        print("=" * 80)
        print(f"ROI-analys för utfall {outcome}")
        print("=" * 80)

        summary = calculate_roi(
            df=df,
            outcome=outcome,
            odds_col=odds_col,
            value_col=value_col
        )

        print(summary.to_string())

    print()
    print("Klar.")


if __name__ == "__main__":
    main()