import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

INPUT_FILE = "english_features.csv"
OUTPUT_FILE = "prematch_probabilities.csv"

NUMERIC_FEATURES = [
    "NormImp1",
    "NormImpX",
    "NormImp2",
    "Overround",
    "HomeFavorite",
    "AwayFavorite",
    "OddsGap",
]

CATEGORICAL_FEATURES = [
    "Division",
]

TARGET = "Outcome"


def main():
    df = pd.read_csv(INPUT_FILE)

    df = df[df[TARGET].isin(["1", "X", "2"])].copy()

    df = df.dropna(
        subset=NUMERIC_FEATURES + CATEGORICAL_FEATURES + [TARGET]
    )

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", LogisticRegression(max_iter=2000))
        ]
    )

    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)
    classes = list(model.named_steps["model"].classes_)

    result_df = X_test.copy()
    result_df["Outcome"] = y_test.values

    result_df["PredProb1"] = probabilities[:, classes.index("1")]
    result_df["PredProbX"] = probabilities[:, classes.index("X")]
    result_df["PredProb2"] = probabilities[:, classes.index("2")]

    result_df["MarketProb1"] = result_df["NormImp1"]
    result_df["MarketProbX"] = result_df["NormImpX"]
    result_df["MarketProb2"] = result_df["NormImp2"]

    result_df["ModelEdge1"] = result_df["PredProb1"] - result_df["MarketProb1"]
    result_df["ModelEdgeX"] = result_df["PredProbX"] - result_df["MarketProbX"]
    result_df["ModelEdge2"] = result_df["PredProb2"] - result_df["MarketProb2"]

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print(f"Skapade {OUTPUT_FILE}")
    print(f"Antal rader: {len(result_df)}")

    print()
    print("Exempel:")
    print(
        result_df[
            [
                "Outcome",
                "PredProb1",
                "PredProbX",
                "PredProb2",
                "MarketProb1",
                "MarketProbX",
                "MarketProb2",
                "ModelEdge1",
                "ModelEdgeX",
                "ModelEdge2",
            ]
        ].head(20).round(4).to_string(index=False)
    )


if __name__ == "__main__":
    main()