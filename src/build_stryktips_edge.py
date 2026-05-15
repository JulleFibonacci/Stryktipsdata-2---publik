import pandas as pd

INPUT_FILE = "stryktips.csv"
OUTPUT_FILE = "stryktips_edge.csv"


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

    return 1 / odds


def main():
    df = pd.read_csv(INPUT_FILE)

    for col in ["Odds1", "OddsX", "Odds2", "Folk1", "FolkX", "Folk2"]:
        df[col] = df[col].apply(to_float)

    df["Imp1"] = df["Odds1"].apply(implied_probability)
    df["ImpX"] = df["OddsX"].apply(implied_probability)
    df["Imp2"] = df["Odds2"].apply(implied_probability)

    df["Overround"] = df["Imp1"] + df["ImpX"] + df["Imp2"]

    df["MarketProb1"] = df["Imp1"] / df["Overround"]
    df["MarketProbX"] = df["ImpX"] / df["Overround"]
    df["MarketProb2"] = df["Imp2"] / df["Overround"]

    df["FolkProb1"] = df["Folk1"] / 100
    df["FolkProbX"] = df["FolkX"] / 100
    df["FolkProb2"] = df["Folk2"] / 100

    df["Edge1"] = df["MarketProb1"] - df["FolkProb1"]
    df["EdgeX"] = df["MarketProbX"] - df["FolkProbX"]
    df["Edge2"] = df["MarketProb2"] - df["FolkProb2"]

    df["BestEdge"] = df[["Edge1", "EdgeX", "Edge2"]].idxmax(axis=1)

    df["BestEdge"] = df["BestEdge"].replace({
        "Edge1": "1",
        "EdgeX": "X",
        "Edge2": "2",
    })

    df["BestEdgeValue"] = df[["Edge1", "EdgeX", "Edge2"]].max(axis=1)

    output_cols = [
        "Match",
        "Home",
        "Away",
        "League",
        "Round",
        "Odds1",
        "OddsX",
        "Odds2",
        "Folk1",
        "FolkX",
        "Folk2",
        "MarketProb1",
        "MarketProbX",
        "MarketProb2",
        "FolkProb1",
        "FolkProbX",
        "FolkProb2",
        "Edge1",
        "EdgeX",
        "Edge2",
        "BestEdge",
        "BestEdgeValue",
    ]

    df[output_cols].to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(f"Skapade {OUTPUT_FILE}")
    print()
    print(
        df[output_cols]
        .sort_values("BestEdgeValue", ascending=False)
        .round(4)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()