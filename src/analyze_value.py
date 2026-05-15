import pandas as pd

INPUT_FILE = "historical_data.csv"
OUTPUT_FILE = "value_analysis.csv"


def to_float(value):
    if pd.isna(value):
        return None

    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def implied_probability(odds):
    if odds is None or pd.isna(odds) or odds <= 1:
        return None

    return 100 / odds


def prepare_data():
    df = pd.read_csv(INPUT_FILE)

    for col in ["Odds1", "OddsX", "Odds2"]:
        df[col] = df[col].apply(to_float)

    for col in ["Folk1", "FolkX", "Folk2"]:
        df[col] = df[col].apply(to_float)

    df["Imp1"] = df["Odds1"].apply(implied_probability)
    df["ImpX"] = df["OddsX"].apply(implied_probability)
    df["Imp2"] = df["Odds2"].apply(implied_probability)

    df["ValueDiff1"] = df["Imp1"] - df["Folk1"]
    df["ValueDiffX"] = df["ImpX"] - df["FolkX"]
    df["ValueDiff2"] = df["Imp2"] - df["Folk2"]

    df["Won1"] = df["Outcome"] == "1"
    df["WonX"] = df["Outcome"] == "X"
    df["Won2"] = df["Outcome"] == "2"

    value_cols = ["ValueDiff1", "ValueDiffX", "ValueDiff2"]

    valid_value_rows = df[value_cols].notna().any(axis=1)

    df["BestValue"] = ""
    df["BestValueDiff"] = None
    df["BestValueWon"] = False

    df.loc[valid_value_rows, "BestValue"] = (
        df.loc[valid_value_rows, value_cols]
        .idxmax(axis=1)
        .replace({
            "ValueDiff1": "1",
            "ValueDiffX": "X",
            "ValueDiff2": "2"
        })
    )

    df.loc[valid_value_rows, "BestValueDiff"] = (
        df.loc[valid_value_rows, value_cols].max(axis=1)
    )

    df.loc[valid_value_rows, "BestValueWon"] = (
        df.loc[valid_value_rows, "Outcome"] == df.loc[valid_value_rows, "BestValue"]
    )

    return df


def print_summary(df):
    print()
    print(f"Läste in {len(df)} historiska matcher från {INPUT_FILE}")
    print(f"Sparar analys till {OUTPUT_FILE}")

    valid_df = df[df["BestValue"] != ""].copy()

    print()
    print(f"Rader med komplett value-data: {len(valid_df)}")
    print(f"Rader utan komplett value-data: {len(df) - len(valid_df)}")

    print()
    print("Sammanfattning BestValue:")

    summary = valid_df.groupby("BestValue").agg(
        Antal=("BestValueWon", "count"),
        Träffprocent=("BestValueWon", "mean"),
        SnittValueDiff=("BestValueDiff", "mean"),
    )

    summary["Träffprocent"] = summary["Träffprocent"] * 100

    print(summary.round(2).to_string())

    print()
    print("Topp 20 högsta value-diff:")

    cols = [
        "DrawNumber",
        "Match",
        "Home",
        "Away",
        "Outcome",
        "Odds1",
        "OddsX",
        "Odds2",
        "Folk1",
        "FolkX",
        "Folk2",
        "Imp1",
        "ImpX",
        "Imp2",
        "ValueDiff1",
        "ValueDiffX",
        "ValueDiff2",
        "BestValue",
        "BestValueDiff",
        "BestValueWon",
    ]

    print(
        valid_df.sort_values("BestValueDiff", ascending=False)
        .head(20)[cols]
        .round(2)
        .to_string(index=False)
    )


def main():
    df = prepare_data()

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print_summary(df)

    print()
    print("Klar.")


if __name__ == "__main__":
    main()