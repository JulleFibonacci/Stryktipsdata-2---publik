import pandas as pd

INPUT_FILE = "stryktips_edge.csv"
OUTPUT_FILE = "stryktips_recommendations.csv"


def classify_risk(row):
    max_market_prob = max(
        row["MarketProb1"],
        row["MarketProbX"],
        row["MarketProb2"]
    )

    if max_market_prob >= 0.60:
        return "Låg"

    if max_market_prob >= 0.45:
        return "Medel"

    return "Hög"


def recommendation_type(row):
    best_edge = row["BestEdge"]
    best_edge_value = row["BestEdgeValue"]

    market_probs = {
        "1": row["MarketProb1"],
        "X": row["MarketProbX"],
        "2": row["MarketProb2"],
    }

    best_market_prob = market_probs[best_edge]

    if best_edge_value >= 0.08 and best_market_prob >= 0.30:
        return "Spik-kandidat"

    if best_edge_value >= 0.05:
        return "Gardera med value-tecken"

    if best_edge_value >= 0.025:
        return "Svag value"

    return "Ingen tydlig value"


def suggested_signs(row):
    probs = {
        "1": row["MarketProb1"],
        "X": row["MarketProbX"],
        "2": row["MarketProb2"],
    }

    edges = {
        "1": row["Edge1"],
        "X": row["EdgeX"],
        "2": row["Edge2"],
    }

    best_edge = row["BestEdge"]

    signs = set()

    signs.add(best_edge)

    for sign, prob in probs.items():
        if prob >= 0.38:
            signs.add(sign)

    for sign, edge in edges.items():
        if edge >= 0.05:
            signs.add(sign)

    order = ["1", "X", "2"]

    return "".join(
        sign for sign in order
        if sign in signs
    )


def main():
    df = pd.read_csv(INPUT_FILE)

    df["Risk"] = df.apply(classify_risk, axis=1)
    df["RecommendationType"] = df.apply(recommendation_type, axis=1)
    df["SuggestedSigns"] = df.apply(suggested_signs, axis=1)

    df = df.sort_values(
        by="BestEdgeValue",
        ascending=False
    )

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
        "Edge1",
        "EdgeX",
        "Edge2",
        "BestEdge",
        "BestEdgeValue",
        "Risk",
        "RecommendationType",
        "SuggestedSigns",
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
        .round(4)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()