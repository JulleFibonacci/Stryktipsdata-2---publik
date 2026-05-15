import pandas as pd

INPUT_FILE = "stryktips_edge.csv"

PROBABILITY_OUTPUT = "probability_model.csv"
VALUE_OUTPUT = "value_model.csv"


def probability_signs(row):
    probs = {
        "1": row["MarketProb1"],
        "X": row["MarketProbX"],
        "2": row["MarketProb2"],
    }

    sorted_probs = sorted(
        probs.items(),
        key=lambda item: item[1],
        reverse=True
    )

    top_sign, top_prob = sorted_probs[0]
    second_sign, second_prob = sorted_probs[1]

    if top_prob >= 0.60:
        return top_sign

    if top_prob >= 0.45:
        return "".join(
            sign for sign in ["1", "X", "2"]
            if sign in [top_sign, second_sign]
        )

    return "1X2"


def value_signs(row):
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

    signs = set()

    best_edge = max(
        edges.items(),
        key=lambda item: item[1]
    )[0]

    signs.add(best_edge)

    for sign, edge in edges.items():
        if edge >= 0.05:
            signs.add(sign)

    for sign, prob in probs.items():
        if prob >= 0.45:
            signs.add(sign)

    return "".join(
        sign for sign in ["1", "X", "2"]
        if sign in signs
    )


def model_reason_probability(row):
    best_prob = max(
        row["MarketProb1"],
        row["MarketProbX"],
        row["MarketProb2"]
    )

    if best_prob >= 0.60:
        return "Stark marknadsfavorit"

    if best_prob >= 0.45:
        return "Tydlig men inte säker marknadsfavorit"

    return "Jämn match enligt marknaden"


def model_reason_value(row):
    best_edge = row["BestEdge"]
    edge_value = row["BestEdgeValue"]

    if edge_value >= 0.08:
        return f"Stark value på {best_edge}: folket underskattar utfallet tydligt"

    if edge_value >= 0.05:
        return f"Bra value på {best_edge}: marknaden ger högre chans än folket"

    if edge_value >= 0.025:
        return f"Svag value på {best_edge}: liten men relevant skillnad"

    return "Ingen tydlig value"


def build_probability_model(df):
    model = df.copy()

    model["Model"] = "Probability"
    model["RecommendedSigns"] = model.apply(probability_signs, axis=1)
    model["Reason"] = model.apply(model_reason_probability, axis=1)

    model["PrimarySign"] = model[
        ["MarketProb1", "MarketProbX", "MarketProb2"]
    ].idxmax(axis=1)

    model["PrimarySign"] = model["PrimarySign"].replace({
        "MarketProb1": "1",
        "MarketProbX": "X",
        "MarketProb2": "2",
    })

    model["PrimaryScore"] = model[
        ["MarketProb1", "MarketProbX", "MarketProb2"]
    ].max(axis=1)

    return model


def build_value_model(df):
    model = df.copy()

    model["Model"] = "Value"
    model["RecommendedSigns"] = model.apply(value_signs, axis=1)
    model["Reason"] = model.apply(model_reason_value, axis=1)
    model["PrimarySign"] = model["BestEdge"]
    model["PrimaryScore"] = model["BestEdgeValue"]

    return model


def export_model(model_df, output_file):
    output_cols = [
        "Model",
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
        "PrimarySign",
        "PrimaryScore",
        "RecommendedSigns",
        "Reason",
    ]

    model_df[output_cols].to_csv(
        output_file,
        index=False
    )

    print()
    print(f"Skapade {output_file}")
    print(
        model_df[output_cols]
        .round(4)
        .to_string(index=False)
    )


def main():
    df = pd.read_csv(INPUT_FILE)

    probability_model = build_probability_model(df)
    value_model = build_value_model(df)

    export_model(
        probability_model,
        PROBABILITY_OUTPUT
    )

    export_model(
        value_model,
        VALUE_OUTPUT
    )


if __name__ == "__main__":
    main()