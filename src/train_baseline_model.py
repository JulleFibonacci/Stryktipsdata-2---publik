import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    log_loss
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

INPUT_FILE = "english_features.csv"

FEATURES = [
    "NormImp1",
    "NormImpX",
    "NormImp2",
    "Overround",
    "HomeFavorite",
    "AwayFavorite",
    "OddsGap",
    "ShotDiff",
    "ShotTargetDiff",
    "CornerDiff",
    "YellowCardDiff",
    "RedCardDiff",
]

TARGET = "Outcome"


def main():
    df = pd.read_csv(INPUT_FILE)

    df = df[
        df[TARGET].isin(["1", "X", "2"])
    ].copy()

    df = df.dropna(
        subset=FEATURES + [TARGET]
    )

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(
                max_iter=2000
            ))
        ]
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)

    print()
    print("Baseline Logistic Regression")
    print("=" * 80)

    print()
    print(f"Antal träningsrader: {len(X_train)}")
    print(f"Antal testrader: {len(X_test)}")

    print()
    print("Accuracy:")
    print(
        round(
            accuracy_score(
                y_test,
                predictions
            ) * 100,
            2
        ),
        "%"
    )

    print()
    print("Log loss:")
    print(
        round(
            log_loss(
                y_test,
                probabilities
            ),
            4
        )
    )

    print()
    print("Classification report:")
    print(
        classification_report(
            y_test,
            predictions
        )
    )

    model_step = model.named_steps["model"]

    feature_importance = pd.DataFrame({
        "Feature": FEATURES,
        "Coef_1": model_step.coef_[0],
        "Coef_2": model_step.coef_[1],
        "Coef_X": model_step.coef_[2],
    })

    print()
    print("Feature coefficients:")
    print(
        feature_importance
        .round(4)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()