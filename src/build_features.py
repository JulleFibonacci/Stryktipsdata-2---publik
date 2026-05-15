import pandas as pd
import numpy as np

INPUT_FILE = "english_football_data.csv"
OUTPUT_FILE = "english_features.csv"


def implied_probability(odds):
    if pd.isna(odds) or odds <= 0:
        return np.nan

    return 1 / odds


def build_features(df):
    # -----------------------------
    # Implied probabilities
    # -----------------------------

    df["Imp1"] = df["Odds1"].apply(implied_probability)
    df["ImpX"] = df["OddsX"].apply(implied_probability)
    df["Imp2"] = df["Odds2"].apply(implied_probability)

    # -----------------------------
    # Overround
    # -----------------------------

    df["Overround"] = (
        df["Imp1"]
        + df["ImpX"]
        + df["Imp2"]
    )

    # -----------------------------
    # Normalized probabilities
    # -----------------------------

    df["NormImp1"] = df["Imp1"] / df["Overround"]
    df["NormImpX"] = df["ImpX"] / df["Overround"]
    df["NormImp2"] = df["Imp2"] / df["Overround"]

    # -----------------------------
    # Favorite flags
    # -----------------------------

    df["HomeFavorite"] = (
        df["Odds1"] < df["Odds2"]
    ).astype(int)

    df["AwayFavorite"] = (
        df["Odds2"] < df["Odds1"]
    ).astype(int)

    # -----------------------------
    # Odds gap
    # -----------------------------

    df["OddsGap"] = (
        df["Odds2"] - df["Odds1"]
    )

    # -----------------------------
    # Goal difference
    # -----------------------------

    df["GoalDiff"] = (
        df["HomeGoals"] - df["AwayGoals"]
    )

    # -----------------------------
    # Shot difference
    # -----------------------------

    df["ShotDiff"] = (
        df["HomeShots"] - df["AwayShots"]
    )

    df["ShotTargetDiff"] = (
        df["HomeShotsTarget"]
        - df["AwayShotsTarget"]
    )

    # -----------------------------
    # Corner difference
    # -----------------------------

    df["CornerDiff"] = (
        df["HomeCorners"]
        - df["AwayCorners"]
    )

    # -----------------------------
    # Card difference
    # -----------------------------

    df["YellowCardDiff"] = (
        df["HomeYellowCards"]
        - df["AwayYellowCards"]
    )

    df["RedCardDiff"] = (
        df["HomeRedCards"]
        - df["AwayRedCards"]
    )

    # -----------------------------
    # Total goals
    # -----------------------------

    df["TotalGoals"] = (
        df["HomeGoals"]
        + df["AwayGoals"]
    )

    # -----------------------------
    # High scoring flag
    # -----------------------------

    df["Over2_5Goals"] = (
        df["TotalGoals"] >= 3
    ).astype(int)

    # -----------------------------
    # Draw flag
    # -----------------------------

    df["IsDraw"] = (
        df["Outcome"] == "X"
    ).astype(int)

    return df


def main():
    df = pd.read_csv(INPUT_FILE)

    numeric_columns = [
        "Odds1",
        "OddsX",
        "Odds2",
        "HomeGoals",
        "AwayGoals",
        "HomeShots",
        "AwayShots",
        "HomeShotsTarget",
        "AwayShotsTarget",
        "HomeCorners",
        "AwayCorners",
        "HomeYellowCards",
        "AwayYellowCards",
        "HomeRedCards",
        "AwayRedCards",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = build_features(df)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(f"Skapade {OUTPUT_FILE}")
    print(f"Antal matcher: {len(df)}")
    print(f"Antal kolumner: {len(df.columns)}")

    print()
    print("Nya features:")
    print()

    feature_columns = [
        "Imp1",
        "ImpX",
        "Imp2",
        "Overround",
        "NormImp1",
        "NormImpX",
        "NormImp2",
        "HomeFavorite",
        "AwayFavorite",
        "OddsGap",
        "GoalDiff",
        "ShotDiff",
        "ShotTargetDiff",
        "CornerDiff",
        "YellowCardDiff",
        "RedCardDiff",
        "TotalGoals",
        "Over2_5Goals",
        "IsDraw",
    ]

    for feature in feature_columns:
        print(f"- {feature}")


if __name__ == "__main__":
    main()