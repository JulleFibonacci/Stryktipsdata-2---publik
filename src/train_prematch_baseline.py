import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, log_loss
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

INPUT_FILE = "english_features.csv"

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

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)

    print()
    print("Prematch Baseline Logistic Regression")
    print("=" * 80)

    print()
    print(f"Antal träningsrader: {len(X_train)}")
    print(f"Antal testrader: {len(X_test)}")

    print()
    print("Accuracy:")
    print(round(accuracy_score(y_test, predictions) * 100, 2), "%")

    print()
    print("Log loss:")
    print(round(log_loss(y_test, probabilities), 4))

    print()
    print("Classification report:")
    print(classification_report(y_test, predictions))

    print()
    print("Klasser:")
    print(model.named_steps["model"].classes_)


if __name__ == "__main__":
    main()