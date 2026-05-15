import pandas as pd

INPUT_FILE = "value_analysis.csv"


SEGMENTS_TO_TEST = [
    {
        "name": "Home underdogs neutral value",
        "outcome": "1",
        "odds_col": "Odds1",
        "value_col": "ValueDiff1",
        "odds_min": 3.0,
        "odds_max": 5.0,
        "value_min": -5,
        "value_max": 5,
    },
    {
        "name": "Away underdogs neutral value",
        "outcome": "2",
        "odds_col": "Odds2",
        "value_col": "ValueDiff2",
        "odds_min": 3.0,
        "odds_max": 5.0,
        "value_min": -5,
        "value_max": 5,
    },
]


PERIODS = [
    (4000, 4299),
    (4300, 4599),
    (4600, 4899),
    (4900, 4999),
]


def calculate_segment(df, segment, start_draw, end_draw):
    data = df[
        (df["DrawNumber"] >= start_draw)
        & (df["DrawNumber"] <= end_draw)
        & df[segment["odds_col"]].notna()
        & df[segment["value_col"]].notna()
        & df["Outcome"].isin(["1", "X", "2"])
    ].copy()

    data = data[
        (data[segment["odds_col"]] >= segment["odds_min"])
        & (data[segment["odds_col"]] <= segment["odds_max"])
        & (data[segment["value_col"]] >= segment["value_min"])
        & (data[segment["value_col"]] <= segment["value_max"])
    ]

    data["Won"] = data["Outcome"] == segment["outcome"]

    data["Profit"] = data.apply(
        lambda row: row[segment["odds_col"]] - 1
        if row["Won"]
        else -1,
        axis=1
    )

    bets = len(data)
    wins = int(data["Won"].sum())
    profit = float(data["Profit"].sum())

    roi = profit / bets * 100 if bets > 0 else 0
    hit_rate = wins / bets * 100 if bets > 0 else 0

    return {
        "Segment": segment["name"],
        "Period": f"{start_draw}-{end_draw}",
        "Bets": bets,
        "Wins": wins,
        "HitRate": round(hit_rate, 2),
        "Profit": round(profit, 2),
        "ROI": round(roi, 2),
    }


def main():
    df = pd.read_csv(INPUT_FILE)

    rows = []

    for segment in SEGMENTS_TO_TEST:
        for start_draw, end_draw in PERIODS:
            rows.append(
                calculate_segment(
                    df=df,
                    segment=segment,
                    start_draw=start_draw,
                    end_draw=end_draw,
                )
            )

    result_df = pd.DataFrame(rows)

    print()
    print("=" * 100)
    print("ROBUSTHETSTEST AV TOPPSEGMENT")
    print("=" * 100)
    print()
    print(result_df.to_string(index=False))

    result_df.to_csv(
        "segment_robustness.csv",
        index=False
    )

    print()
    print("Skapade segment_robustness.csv")


if __name__ == "__main__":
    main()